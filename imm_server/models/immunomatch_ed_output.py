# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from imm_server.models.base_model_ import Model
from imm_server.models.feature_data_out import FeatureDataOut  # noqa: F401,E501
from imm_server import util


class ImmunomatchEdOutput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, immunoscore: int=None, risk_category: str=None, guidance: str=None, readiness_flag: bool=None, features_used: List[FeatureDataOut]=None):  # noqa: E501
        """ImmunomatchEdOutput - a model defined in Swagger

        :param immunoscore: The immunoscore of this ImmunomatchEdOutput.  # noqa: E501
        :type immunoscore: int
        :param risk_category: The risk_category of this ImmunomatchEdOutput.  # noqa: E501
        :type risk_category: str
        :param guidance: The guidance of this ImmunomatchEdOutput.  # noqa: E501
        :type guidance: str
        :param readiness_flag: The readiness_flag of this ImmunomatchEdOutput.  # noqa: E501
        :type readiness_flag: bool
        :param features_used: The features_used of this ImmunomatchEdOutput.  # noqa: E501
        :type features_used: List[FeatureDataOut]
        """
        self.swagger_types = {
            'immunoscore': int,
            'risk_category': str,
            'guidance': str,
            'readiness_flag': bool,
            'features_used': List[FeatureDataOut]
        }

        self.attribute_map = {
            'immunoscore': 'immunoscore',
            'risk_category': 'risk_category',
            'guidance': 'guidance',
            'readiness_flag': 'readiness_flag',
            'features_used': 'features_used'
        }
        self._immunoscore = immunoscore
        self._risk_category = risk_category
        self._guidance = guidance
        self._readiness_flag = readiness_flag
        self._features_used = features_used

    @classmethod
    def from_dict(cls, dikt) -> 'ImmunomatchEdOutput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The immunomatch_ed_output of this ImmunomatchEdOutput.  # noqa: E501
        :rtype: ImmunomatchEdOutput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def immunoscore(self) -> int:
        """Gets the immunoscore of this ImmunomatchEdOutput.

        ImmunoScore Value  # noqa: E501

        :return: The immunoscore of this ImmunomatchEdOutput.
        :rtype: int
        """
        return self._immunoscore

    @immunoscore.setter
    def immunoscore(self, immunoscore: int):
        """Sets the immunoscore of this ImmunomatchEdOutput.

        ImmunoScore Value  # noqa: E501

        :param immunoscore: The immunoscore of this ImmunomatchEdOutput.
        :type immunoscore: int
        """
        if immunoscore is None:
            raise ValueError("Invalid value for `immunoscore`, must not be `None`")  # noqa: E501

        self._immunoscore = immunoscore

    @property
    def risk_category(self) -> str:
        """Gets the risk_category of this ImmunomatchEdOutput.

        Risk Category  # noqa: E501

        :return: The risk_category of this ImmunomatchEdOutput.
        :rtype: str
        """
        return self._risk_category

    @risk_category.setter
    def risk_category(self, risk_category: str):
        """Sets the risk_category of this ImmunomatchEdOutput.

        Risk Category  # noqa: E501

        :param risk_category: The risk_category of this ImmunomatchEdOutput.
        :type risk_category: str
        """
        allowed_values = ["low", "medium", "high"]  # noqa: E501
        if risk_category not in allowed_values:
            raise ValueError(
                "Invalid value for `risk_category` ({0}), must be one of {1}"
                .format(risk_category, allowed_values)
            )

        self._risk_category = risk_category

    @property
    def guidance(self) -> str:
        """Gets the guidance of this ImmunomatchEdOutput.

        Text with guidance for provider associated with risk category  # noqa: E501

        :return: The guidance of this ImmunomatchEdOutput.
        :rtype: str
        """
        return self._guidance

    @guidance.setter
    def guidance(self, guidance: str):
        """Sets the guidance of this ImmunomatchEdOutput.

        Text with guidance for provider associated with risk category  # noqa: E501

        :param guidance: The guidance of this ImmunomatchEdOutput.
        :type guidance: str
        """
        if guidance is None:
            raise ValueError("Invalid value for `guidance`, must not be `None`")  # noqa: E501

        self._guidance = guidance

    @property
    def readiness_flag(self) -> bool:
        """Gets the readiness_flag of this ImmunomatchEdOutput.

        Flag that turns true if the immunoscore value is ready to be displayed and used. In the flag is false, the immonoscore is too inaccurate.  # noqa: E501

        :return: The readiness_flag of this ImmunomatchEdOutput.
        :rtype: bool
        """
        return self._readiness_flag

    @readiness_flag.setter
    def readiness_flag(self, readiness_flag: bool):
        """Sets the readiness_flag of this ImmunomatchEdOutput.

        Flag that turns true if the immunoscore value is ready to be displayed and used. In the flag is false, the immonoscore is too inaccurate.  # noqa: E501

        :param readiness_flag: The readiness_flag of this ImmunomatchEdOutput.
        :type readiness_flag: bool
        """
        if readiness_flag is None:
            raise ValueError("Invalid value for `readiness_flag`, must not be `None`")  # noqa: E501

        self._readiness_flag = readiness_flag

    @property
    def features_used(self) -> List[FeatureDataOut]:
        """Gets the features_used of this ImmunomatchEdOutput.

        Array of features used for algorithm.  # noqa: E501

        :return: The features_used of this ImmunomatchEdOutput.
        :rtype: List[FeatureDataOut]
        """
        return self._features_used

    @features_used.setter
    def features_used(self, features_used: List[FeatureDataOut]):
        """Sets the features_used of this ImmunomatchEdOutput.

        Array of features used for algorithm.  # noqa: E501

        :param features_used: The features_used of this ImmunomatchEdOutput.
        :type features_used: List[FeatureDataOut]
        """
        if features_used is None:
            raise ValueError("Invalid value for `features_used`, must not be `None`")  # noqa: E501

        self._features_used = features_used
