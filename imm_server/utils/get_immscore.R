library(jsonlite)
library(dplyr)
library(ranger)
library(stringr)
library(data.table)

get_immscore = function(query){
	query = fromJSON(query)
	dat = read.csv("biom_df.csv")
	for(i in 1:ncol(dat)){
	  dat[is.na(dat[,i]),i] <- mean(dat[,i], na.rm = TRUE)
	}
	dat = dat[!names(dat) %in% c("X")]
	## add features from json data into train data
	queryList = type.convert(as.list(unlist(query)), as.is = TRUE)
	names(queryList) = str_remove(names(queryList), 'features\\.')
	names(queryList) = str_remove(names(queryList), '.value')
	queryList = queryList[-c(1,3,4)]
	nm1 = setdiff(intersect(names(dat), names(queryList)), 'subject')
	nm2 = setdiff(names(queryList), names(dat))
	setDT(dat)[as.data.table(queryList), (nm1):= mget(paste0("i.", nm1)), on = .(subject)]
	dat[as.data.table(queryList), (nm2):=mget(nm2), on=.(subject)]
	dat = dat[!names(dat) %in% c("subject")]
	
	## feature ranges
	features  = c("ap6xl", "pct5", "crp4", "age", "temperature_value", "heartrate_value", "gcst_value")
	proteins = c("ap6xl", "pct5", "crp4", "gcst_value")
	i=0
	limit=0.05
	features_used=list()
	for (fet in features)
	{
	  i=i+1
	  #print(fet)
	  d=dat[,fet]
	  q=quantile(d,probs=c(0,limit/2,0.25,0.5,0.75,1-limit/2,1),na.rm = TRUE)
	  #print(q)
	  if (fet %in% proteins) {
	    breaks=10^seq(log10(q[1]),log10(q[7]),length.out=10)
	  } else {
	    breaks=seq(q[1],q[7],length.out=10)
	  }
	  #print(breaks)
	  r=table(cut(d, breaks=breaks))
	  r=as.data.frame(r)
	  r$value=diff(breaks)/2+breaks[1:(length(breaks)-1)]
	  r$Prop=r$Freq/sum(r$Freq)
	  
	  #print(r)
	  feature_used=list(
	    name=fet,
	    value=NA,
	    range_value=r$value,
	    range_frequency=r$Prop,#/max(r$Prop)*100,
	    importance=0
	  )
	  features_used[[i]]=feature_used
	}
	
	features_ranges=list(features_used=features_used)
	feature_used = features_ranges$features_used
	feature_used = Filter(function(x) max(x <- x$range_value) <= 100 & min(x >= 0), feature_used)
	
	fitControl <- trainControl(method = "repeatedcv",number = 10,repeats = 5, search = "random")
	model_cv <- train(gcst_value ~ .,data = dat,method = "lm",trControl = fitControl,na.action = na.omit)
	immunoscore = predict(model_cv, dat)
	
	guidance = "available by request"
	readiness_flag= FALSE
	risk_category = "medium"
	
	immEd_output = list(
	  immunoscore = immunoscore,
	  risk_category = risk_category,
	  guidance = guidance,
	  readiness_flag = readiness_flag,
	  feature_used = feature_used
	)
	
	immEd_output = toJSON(immEd_output)
	return(immEd_output)
}