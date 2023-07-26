import os

import pytest
import savers
from tests import data
import log_utils


# A lot of copypasta, needs refactoring
@pytest.fixture
def csv_saver() -> savers.CSVSaver:
    tmp_path = 'some_path'  # temporary path, which will be replaced
    saver = savers.CSVSaver(tmp_path)
    return saver


@pytest.fixture
def tsv_saver() -> savers.TSVSaver:
    tmp_path = 'some_path'  # temporary path, which will be replaced
    saver = savers.TSVSaver(tmp_path)
    return saver


@pytest.mark.parametrize(
    'reference_path, test_path, save_data',
    [
        # Test case 1: ...
        ('ref_files/ref1', 'test_files/test1',
         data.SAVE_DATA1),

        # Test case 2: ...
        # (),
    ],
)
def test_csv_saver_save(csv_saver, reference_path, test_path, save_data):
    csv_saver._output_path = test_path
    log_utils.logger.debug(csv_saver._output_path)
    csv_saver.save(save_data)

    reference_file_data = read_data_from_file(reference_path, 'csv')
    actual_file_data = read_data_from_file(test_path, 'csv')

    assert reference_file_data == actual_file_data


@pytest.mark.parametrize(
    'reference_path, test_path, save_data',
    [
        # Test case 1: ...
        ('ref_files/ref1', 'test_files/test1',
         data.SAVE_DATA1),

        # Test case 2: ...
        # (),
    ],
)
def test_tsv_saver_save(tsv_saver, reference_path, test_path, save_data):
    tsv_saver._output_path = test_path
    log_utils.logger.debug(tsv_saver._output_path)
    tsv_saver.save(save_data)

    reference_file_data = read_data_from_file(reference_path, 'tsv')
    actual_file_data = read_data_from_file(test_path, 'tsv')

    assert reference_file_data == actual_file_data


def read_data_from_file(path: str,
                        format: str,
                        ) -> list[str]:
    with open(f"{path}.{format}", 'r', encoding='utf-8') as file:
        return file.readlines()


if __name__ == '__main__':
    pytest.main()
