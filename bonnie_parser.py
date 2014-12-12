__author__ = 'savex'

import sys
import csv

from src.utils.file import *

b_01_sq_out_chr_str = "Sequential Output,Per character"
b_02_sq_out_bl_str = "Sequential Output,Block"
b_03_sq_out_rw_str = "Sequential Output,Rewrite"
b_04_sq_in_chr_str = "Sequential Input,Per character"
b_05_sq_in_bl_str = "Sequential Input,Block"
b_06_rnd_seek_str = "Random,Seeks"
b_07_sq_crt_str = "Sequential Create,Create"
b_08_sq_crt_r_str = "Sequential Create,Read"
b_09_sq_crt_del_str = "Sequential Create,Delete"
b_10_rnd_crt_str = "Random create,Create"
b_11_rnd_crt_r_str = "Random create,Read"
b_12_rnd_crt_del_str = "Random create,Delete"


def help_message():
    print"Please, supply log file folder name as an only parameter"

    return

def _csv_data(filename, load_all=False):
    delimiter = ','
    # field names
    _names = read_file_as_lines(os.path.join('bonnie', '_bonnie_template.csv'))[0].split(delimiter)
    #file with raw data
    lines = read_file_as_lines(filename)
    #built in reader with output as dict
    _csv_dict = csv.DictReader(
        lines,
        fieldnames=_names,
        delimiter=delimiter
    )
    if load_all:
        list = []
        for item in _csv_dict:
            if item['version'] == '1.96':
                list.append(item)
        return list
    else:
        # iterate to find line with parse-able data
        for item in _csv_dict:
            if item['version'] == '1.96':
                return item

    return None

def load_result_from_file(filename):
    _volume_result_dict = {}

    _csv_data_list = _csv_data(filename, load_all=True)

    _items = dict(
                concurrency="1",
                volume_name="VDC",
                vm_name="bonnie_vm",
            )

    _results = {}

    for index in range(0, _csv_data_list.__len__()):
        _results[index] = []
        _item = dict(_items.items() + _csv_data_list[index].items())
        # out
        _results[index].append(_item)
    return _results

def _load_from_folder(folder, single_mode=True):
    _files = {}

    _folder_content = os.listdir(folder)

    # sort them by number of simultaneous volumes
    # single mode
    for _filename in _folder_content:

        _concurency = int(_filename.split('.')[0].rsplit('_', 1)[1])
        _volume_name = _filename.split('.')[0].rsplit('_', 2)[1]
        _vm_name = _filename.split('.')[0].rsplit('_', 3)[1]

        if not _files.has_key(_concurency):
            _files[_concurency] = []
        _files[_concurency].append(
            dict(
                concurrency=_concurency,
                volume_name=_volume_name.upper(),
                vm_name=_vm_name,
                filename=_filename
            )
        )

    _results = {}
    for _concurency in _files.keys():
        _results[_concurency] = []
        for _file in _files[_concurency]:
            #load csv data from file

            _values = _csv_data(os.path.join(folder, _file['filename']))
            if _values is not None:
                #parse csv data into dict
                _file = dict(_file.items() + _values.items())
            # out
            _results[_concurency].append(_file)

    return _results


def _wc(string):
    return string + ','

def parse_results_to_file(results_dict, filename_prefix):
    # write csv file for our document
    # In result document we should have
    # value_name, value_subname, concurency, vm_name,
    _line_prefixes = []
    # per concurrency result name

    # _line_prefixes.append(b_01_sq_out_chr_str)
    _line_prefixes.append(b_02_sq_out_bl_str)
    _line_prefixes.append(b_03_sq_out_rw_str)
    # _line_prefixes.append(b_04_sq_in_chr_str)
    _line_prefixes.append(b_05_sq_in_bl_str)
    _line_prefixes.append(b_06_rnd_seek_str)
    # _line_prefixes.append(b_07_sq_crt_str)
    # _line_prefixes.append(b_08_sq_crt_r_str)
    # _line_prefixes.append(b_09_sq_crt_del_str)
    # _line_prefixes.append(b_10_rnd_crt_str)
    # _line_prefixes.append(b_11_rnd_crt_r_str)
    # _line_prefixes.append(b_12_rnd_crt_del_str)

    _results = results_dict.keys()

    # detect maximum columns
    columns_count = 3
    _vol_len_out = 4
    for result in _results:
        _vol_len = 4
        for _vol in results_dict[result]:
            if _vol_len < _vol.__len__()*4:
                _vol_len_out = _vol_len * 4
    columns_count += _vol_len_out

    for result in _results:
        # prepare header line
        _header = []

        _header.append('Method')
        _header.append('Sub name')
        _header.append('Concurrency')

        for _volume_result in results_dict[result]:
            _header.append(_volume_result['vm_name'])
            _header.append(_volume_result['volume_name'] + "_Ksec")
            _header.append(_volume_result['volume_name'] + "_%CPU")
            _header.append(_volume_result['volume_name'] + "_Latency")

        _header_str = ",".join(_header)
        _filename_res = filename_prefix + '.csv'

        append_line_to_file(_filename_res, _header_str)

        # collect values and write them
        for index in range(0, _line_prefixes.__len__()):
            _list = []

            _list.append(_line_prefixes[index])
            #concurrency value
            _list.append(str(result))

            # iterate volumes
            for _volume_result in results_dict[result]:
                _list.append(_volume_result['vm_name'])

                try:
                    # iterate correct value
                    if _line_prefixes[index] == b_01_sq_out_chr_str:
                        # seq_out_perchar
                        _list.append(_volume_result['seq_out_per-chr_Ksec'])
                        _list.append(_volume_result['seq_out_per-chr_cpu'])
                        _list.append(_volume_result['seq_out_per-chr_ltcy'])
                    elif _line_prefixes[index] == b_02_sq_out_bl_str:
                        # seq_out_block
                        _list.append(_volume_result['seq_out_block_Ksec'])
                        _list.append(_volume_result['seq_out_block_cpu'])
                        _list.append(_volume_result['seq_out_block_ltcy'])
                    elif _line_prefixes[index] == b_03_sq_out_rw_str:
                        # seq_out_rewrite
                        _list.append(_volume_result['seq_out_rewrite_Ksec'])
                        _list.append(_volume_result['seq_out_rewrite_cpu'])
                        _list.append(_volume_result['seq_out_rewrite_ltcy'])
                    elif _line_prefixes[index] == b_04_sq_in_chr_str:
                        # seq_in_perchar
                        _list.append(_volume_result['seq_in_per-chr_Ksec'])
                        _list.append(_volume_result['seq_in_per-chr_cpu'])
                        _list.append(_volume_result['seq_in_per-chr_ltcy'])
                    elif _line_prefixes[index] == b_05_sq_in_bl_str:
                        # seq_in_block
                        _list.append(_volume_result['seq_in_block_Ksec'])
                        _list.append(_volume_result['seq_in_block_cpu'])
                        _list.append(_volume_result['seq_in_block_ltcy'])
                    elif _line_prefixes[index] == b_06_rnd_seek_str:
                        # random_seeks
                        _list.append(_volume_result['random_Ksec'])
                        _list.append(_volume_result['random_cpu'])
                        _list.append(_volume_result['random_ltcy'])
                    elif _line_prefixes[index] == b_07_sq_crt_str:
                        # seq_create_create
                        _list.append(_volume_result['seq_create_create_Ksec'])
                        _list.append(_volume_result['seq_create_create_cpu'])
                        _list.append(_volume_result['seq_create_create_ltcy'])
                    elif _line_prefixes[index] == b_08_sq_crt_r_str:
                        # seq_create_read
                        _list.append(_volume_result['seq_create_read_Ksec'])
                        _list.append(_volume_result['seq_create_read_cpu'])
                        _list.append(_volume_result['seq_create_read_ltcy'])
                    elif _line_prefixes[index] == b_09_sq_crt_del_str:
                        # seq_create_delete
                        _list.append(_volume_result['seq_create_delete_Ksec'])
                        _list.append(_volume_result['seq_create_delete_cpu'])
                        _list.append(_volume_result['seq_create_delete_ltcy'])
                    elif _line_prefixes[index] == b_10_rnd_crt_str:
                        # random_create_create
                        _list.append(_volume_result['random_create_create_Ksec'])
                        _list.append(_volume_result['random_create_create_cpu'])
                        _list.append(_volume_result['random_create_create_ltcy'])
                    elif _line_prefixes[index] == b_11_rnd_crt_r_str:
                        # random_create_read
                        _list.append(_volume_result['random_create_read_Ksec'])
                        _list.append(_volume_result['random_create_read_cpu'])
                        _list.append(_volume_result['random_create_read_ltcy'])
                    elif _line_prefixes[index] == b_12_rnd_crt_del_str:
                        # random_create_delete
                        _list.append(_volume_result['random_create_delete_Ksec'])
                        _list.append(_volume_result['random_create_delete_cpu'])
                        _list.append(_volume_result['random_create_delete_ltcy'])
                except KeyError as e:
                    print("Empty file found: {0}".format(_volume_result['filename']))
                    _list.append("0")

            # count remaining commas
            _line_str = ",".join(_list)
            _columns_to_add = columns_count - _list.__len__()
            # add them if needed
            if _columns_to_add > 0:
                for i in range(1, _columns_to_add):
                    _line_str += ','

            #write line to file_
            append_line_to_file(_filename_res, _line_str)



def bonnie_parser_main():
    print("Bonnie output parser, v0.1")
    # get parameter, exit on error
    if sys.argv.__len__() < 2:
        help_message()

        return

    _file_or_folder = sys.argv[1]

    if os.path.isfile(_file_or_folder):
        _results_list = load_result_from_file(_file_or_folder)
        _filename_prefix = "_".join(["bonnie", "long", "compute"])

        parse_results_to_file(_results_list, _filename_prefix)
    else:

        results_dict = _load_from_folder(_file_or_folder)

        _filename_prefix = "_".join(["bonnie", "compute", "1", "5"])
        parse_results_to_file(results_dict, _filename_prefix)

    return


if __name__ == '__main__':
    bonnie_parser_main()
    # sys.exit(0)
