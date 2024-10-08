from typing import Any, Dict, List, Optional

import pandas as pd
from pandas import DataFrame

from pragman.payload import TextPayload
from pragman.misc.utils import flatten_dict
from pragman.sink.base_sink import BaseSink, BaseSinkConfig, Convertor


class PandasConvertor(Convertor):
    def convert(
        self,
        analyzer_response: TextPayload,
        base_payload: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        base_payload = base_payload or {}
        merged_dict = {**base_payload, **analyzer_response.to_dict()}
        return flatten_dict(merged_dict)


class PandasSinkConfig(BaseSinkConfig):
    TYPE: str = "Pandas"
    dataframe: Optional[DataFrame] = None
    # By default it will include all the columns
    include_columns_list: Optional[List[str]] = None

    def __init__(self, **data: Any):
        super().__init__(**data)

        if self.dataframe is None:
            self.dataframe = DataFrame()


class PandasSink(BaseSink):
    TYPE: str = "Pandas"

    def __init__(self, convertor: Convertor = PandasConvertor(), **data: Any):
        super().__init__(convertor=convertor, **data)

    def send_data(  # type: ignore[override]
        self,
        analyzer_responses: List[TextPayload],
        config: PandasSinkConfig,
        **kwargs: Any,
    ) -> Any:
        responses = []
        for analyzer_response in analyzer_responses:
            converted_response = self.convertor.convert(
                analyzer_response=analyzer_response
            )
            response: Optional[Dict[str, Any]] = None
            if config.include_columns_list:
                response = dict()
                for k, v in converted_response.items():
                    if k in config.include_columns_list:
                        response[k] = v
            else:
                response = converted_response
            responses.append(response)

        if config.dataframe is not None:
            config.dataframe = pd.concat([config.dataframe,pd.DataFrame(responses)], ignore_index=True) # having some issues with the below append code new code
            #config.dataframe = config.dataframe.append(responses)

            # If i will use this append after method and then try to download the dataframe there will be some eror
        
        # # For testing purpose I am checking this DataFrame to csv file code remove this if not required
        config.dataframe.to_csv('output.csv, index=False')

        return config.dataframe