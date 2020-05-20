immunomatch_ed = """

library(jsonlite)
library("dplyr")
library("ranger")

immscore <- function(query){
  query = fromJSON(query)
  data = query$body
  
  ## load models
  models=readRDS("data/model.RDS")
  model=models[[1]][[1]]
  features_in_model=names(model$variable.importance)
  
  ## load emr dataframe
  s1c_2a_3c_l1_biomarker_data = read.csv("data/set1C_2A_3C_l1_biomarker_df.csv")
  wide_emr_data_15094p = read.csv("data/all_patient_wide_df_15094p.csv")
  wide_emr_data_967987 = read.csv("data/all_patient_wide_df_967987.csv")
  wide_emr_data = rbind(wide_emr_data_15094p,wide_emr_data_967987)
  
  long_emr_data_15094p = read.csv("data/all_patient_long_df_15094p.csv")
  long_emr_data_967987 = read.csv("data/all_patient_long_df_967987.csv")
  long_emr_data = rbind(long_emr_data_15094p,long_emr_data_967987)
  
  
  all_emr_data = left_join(wide_emr_data, long_emr_data, by = 'subject') %>% as.data.frame()
  all_emr_s1c_2a_3c_l1_biomarker_data = inner_join(s1c_2a_3c_l1_biomarker_data, wide_emr_data, by = 'subject') %>% left_join(long_emr_data, by = c('subject', 'draw_time_rta', 'rank')) %>% as.data.frame()
  emr_s1c_2a_3c_l1_biomarker_admission_data = all_emr_s1c_2a_3c_l1_biomarker_data %>% filter(rank == 1) %>% as.data.frame()
  
  ## feature range
  limit=0.05
  
  ## Features
  proteins=c("pct5plex_concentration","il6xl_concentration","crp_concentration")
  Vitals=c("temperature_value","heartrate_value","respiratoryrate_value","systolicbp_value","diastolicbp_value","pulseoximetry_value")
  CBC=c("platelets_value","wbc_value","monocyte_value","neutrophil_value")
  CMP=c("bilirubin_value","creatinine_value","glucose_value","bun_value","sodium_value","potassium_value","albumin_value","pH_value")
  Other_labs=c("lactate_value","gcstotal_value")
  features=c(proteins,CBC,CMP,Vitals,Other_labs)
  
  ## feature range calculation
  i=0
  features_used=list()
  for (fet in features)
  {
    i=i+1
    d=emr_s1c_2a_3c_l1_biomarker_admission_data[,fet]
    q=quantile(d,probs=c(0,limit/2,0.25,0.5,0.75,1-limit/2,1),na.rm = TRUE)
    if (fet %in% proteins) {
      breaks=10^seq(log10(q[1]),log10(q[7]),length.out=10)
    } else {
      breaks=seq(q[1],q[7],length.out=10)
    }
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
  
  ## feature ranges
  features_ranges=list(features_used=features_used)
  
  ##
  featuresRanges<-function(features_ranges,feature)
  {
    out=NULL
    for (i in 1:length(features_ranges$features_used))
    {
      
      if(grepl(feature,features_ranges$features_used[[i]]$name,ignore.case = TRUE))
      {
        out=list(range_value=unlist(features_ranges$features_used[[i]]$range_value),range_frequency=unlist(features_ranges$features_used[[i]]$range_frequency))
      }
    }
    return(out)
  }
  
  ##
  feat=data$features
  nam=names(feat)
  features_used=list()
  i=0
  for (fet in nam)
  {
    feature_range=featuresRanges(features_ranges,fet)
    
    if(!is.null(feature_range))
    {
      i=i+1
      if(length(feat[[fet]])>1){
        feature_used=list(
          name=fet,
          value=feat[[fet]]$value,
          range_value=feature_range$range_value,#c(1,10,100,1000,10000),
          range_frequency=feature_range$range_frequency,#c(100,10,3,2,1),
          importance=i
        )
        features_used[[i]]=feature_used
      }
    }
  }
  ## immunoscore
  values=NULL
  nam1=NULL
  for (fet in unique(names(feat))){
    i=grep(fet,features_in_model,ignore.case = TRUE)
    if (fet=="age") {
      val=feat[[fet]]
    } else if (fet=="gender") {
      if (feat[[fet]]=="M") {
        val=1
      } else {
        val=0
      }
    } else {
      val=feat[[fet]]$value
    }
    if(features_in_model[i] %in% proteins)
    {
      val=log10(val)
    }
    values=c(values,val)
    nam1=c(nam1,features_in_model[i])
  }
  for (fet in features_in_model){
    if (!(fet %in% nam1)){
      values=c(values,mean(emr_s1c_2a_3c_l1_biomarker_admission_data[,fet],na.rm = TRUE))
      nam1=c(nam1,fet)
    }
  }
  ## run the model
  names(values)<-nam1
  data_in=as.data.frame(t(values))
  immunoscore=model$predictions[,2]
  
  risk_category="low"
  if (immunoscore>0.35) {
    risk_category="medium"
  }
  if (immunoscore>0.65) {
    risk_category="high"
  }
  
  immunoscore=approx(sort(model$predictions[,2]),seq(1,nrow(model$predictions),1)/nrow(model$predictions),immunoscore)$y*100
  guidance="text description"
  readiness_flag=TRUE
  
  ## immunomatch_ed output
  output=list(
    immunoscore=immunoscore[1:5],
    risk_category=risk_category,
    guidance=guidance,
    readiness_flag=readiness_flag,
    features_used=feature_used
  )
  output = toJSON(output,pretty = TRUE,auto_unbox=TRUE)
  # data_in = toJSON(data_in, pretty = TRUE)
  return(output)
}
"""