import io
import time
import numpy as np
import streamlit as st
from function import DataPreparation, DataProcessing, GetParamAPI, Helper


def GetDataTopexMessage(message, cache: dict):
    data_param_topex = GetParamAPI.GetDataTopexParam(message)
    cache, data_param_topex = Helper.CheckCache(cache, data_param_topex)

    params_none, message = Helper.CheckParamMessage(**data_param_topex)
    result = ''

    check_coordinate = Helper.CheckCoordinate(data_param_topex)

    if check_coordinate:
        if len(params_none) == 0:
            grav_dataset, topo_dataset, topex_dataset = DataPreparation.GetDataTopexAll(cache)

            cache['RawDataType'] = cache['RawDataType'].lower()

            if ('gravity' in cache['RawDataType']) or ('gravitational' in cache['RawDataType']):
                message = 'Here the gravitational data that we successfully get.'
                result = topex_dataset[['Easting', 'Northing', 'GravDataFAA']]

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

                cache['question'] = 'True'

            elif ('topo' in cache['RawDataType']) or ('topography' in cache['RawDataType']):
                message = 'Here the topography data that we successfully get.'
                result = topex_dataset[['Easting', 'Northing', 'TopoData']]

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

                cache['question'] = 'True'

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

                cache['question'] = 'True'

        else:
            st.write_stream(Helper.GeneratorMessage(message))
            cache['question'] = 'False'

    else:
        message = 'Please check your coordinate data. The valid coordinate is north > south and west < east.'
        result = ''
        cache['question'] = 'False'

        st.write_stream(Helper.GeneratorMessage(message))

    return message, result, cache


def GetBougerDensityMessage(message, cache: dict):
    if str(cache['GravDataFAA']) == '' or str(cache['TopoData']) == '':
        list_param = ''

        if str(cache['GravDataFAA']) == '':
            list_param += 'gravity'
        elif str(cache['TopoData']) == '':
            list_param += 'topography'
        elif str(cache['GravDataFAA']) == '' or str(cache['TopoData']) == '':
            list_param += 'gravity and topography'

        message = ("We don't have the gravity data that you want to process. Please upload you gravity and topography "
                   "data or provide the coordinate boundary (north, south, west, and east) that you want to process")
        result = ''
        cache['question'] = 'False'

    else:
        data_param_bouger = GetParamAPI.GetBougerDensityParam(message)
        cache, data_param_bouger = Helper.CheckCache(cache, data_param_bouger)

        params_none, message = Helper.CheckParamMessage(**data_param_bouger)
        result = ''

        check_coordinate = Helper.CheckCoordinate(data_param_bouger)

        if check_coordinate:
            if len(params_none) == 0:
                grav_dataset, topo_dataset, topex_dataset = DataPreparation.GetDataTopexAll(cache)

                message = 'Here the Bouger Density that we successfully processed.'
                RhoBouger = DataProcessing.GetBougerDensity(grav_dataset, topo_dataset)
                result = topex_dataset
                result['RhoBourger'] = RhoBouger

                data_type = cache['RawDataType']
                data_num = Helper.GetNumberUnique(cache['unique_num'])
                cache['unique_num'].append(data_num)

                st.write_stream(Helper.GeneratorMessage(message))
                st.dataframe(result)

                # Create a download button
                st.download_button(
                    key=f'rho_bouger_download_data_{data_num}',
                    label=f'Download data as CSV',
                    data=Helper.ConvertDataDownload(result),
                    file_name=f'data_rho_bourger.csv',
                    mime='text/csv'
                )

                cache['question'] = 'True'

            else:
                st.write_stream(Helper.GeneratorMessage(message))
                cache['question'] = 'False'

        else:
            message = 'Please check your coordinate data. The valid coordinate is north > south and west < east.'
            result = ''
            cache['question'] = 'False'

    return message, result, cache
