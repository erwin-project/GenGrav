import io
import time
import numpy as np
import streamlit as st
from function import DataPreparation, GetParamAPI, Helper


def GetDataTopexMessage(message, cache: dict):
    data_param_topex = GetParamAPI.GetDataTopexParam(message)
    cache, data_param_topex = Helper.CheckCache(cache, data_param_topex)

    params_none, message = Helper.CheckParamMessage(**data_param_topex)
    result = ''

    check_coordinate = Helper.CheckCoordinate(data_param_topex)

    if check_coordinate:
        if len(params_none) == 0:
            if str(cache['GravDataFAA']) == '':
                grav_dataset, topo_dataset, topex_dataset = DataPreparation.GetDataTopex(
                    cache['north'],
                    cache['south'],
                    cache['west'],
                    cache['east']
                )

                cache['GravDataFAA'] = topex_dataset[['easting', 'northing', 'grav_value']]
                cache['TopoData'] = topex_dataset[['easting', 'northing', 'topo_value']]
                cache['TopexData'] = topex_dataset

            else:
                grav_dataset = cache['GravDataFAA']
                topo_dataset = cache['TopoData']
                topex_dataset = cache['TopexData']

            cache['RawDataType'] = cache['RawDataType'].lower()

            if ('gravity' in cache['RawDataType']) or ('gravitational' in cache['RawDataType']):
                message = 'Here the gravitational data that we successfully get.'
                result = grav_dataset

                data_type = cache['RawDataType']
                data_num = Helper.GetNumberUnique(cache['unique_num'])
                cache['unique_num'].append(data_num)

                st.write_stream(Helper.GeneratorMessage(message))
                st.dataframe(result)

                # Create a download button
                st.download_button(
                    key=f'grav_download_data_{data_num}',
                    label=f'Download data as CSV',
                    data=Helper.ConvertDataDownload(result),
                    file_name=f'data_{data_type}.csv',
                    mime='text/csv'
                )

            elif ('topo' in cache['RawDataType']) or ('topography' in cache['RawDataType']):
                message = 'Here the topography data that we successfully get.'
                result = topo_dataset

                data_type = cache['RawDataType']
                data_num = Helper.GetNumberUnique(cache['unique_num'])
                cache['unique_num'].append(data_num)

                st.write_stream(Helper.GeneratorMessage(message))
                st.dataframe(result)

                # Create a download button
                st.download_button(
                    key=f'topo_download_data_{data_num}',
                    label=f'Download data as CSV',
                    data=Helper.ConvertDataDownload(result),
                    file_name=f'data_{data_type}.csv',
                    mime='text/csv'
                )

            else:
                message = 'Here the gravitational and topography data that we successfully get.'
                result = topex_dataset

                data_type = cache['RawDataType']
                data_num = Helper.GetNumberUnique(cache['unique_num'])
                cache['unique_num'].append(data_num)

                st.write_stream(Helper.GeneratorMessage(message))
                st.dataframe(result)

                # Create a download button
                st.download_button(
                    key=f'topex_download_data_{data_num}',
                    label=f'Download data as CSV',
                    data=Helper.ConvertDataDownload(result),
                    file_name=f'data_{data_type}.csv',
                    mime='text/csv'
                )
        else:
            st.write_stream(Helper.GeneratorMessage(message))
    else:
        message = 'Please check your coordinate data. The valid coordinate is north > south and west < east.'
        result = ''

        st.write_stream(Helper.GeneratorMessage(message))

    return message, result, cache


def GetBougerDensityMessage(message, cache: dict):
    return None