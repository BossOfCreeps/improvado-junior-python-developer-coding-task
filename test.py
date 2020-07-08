from classes.CSV import CSV
from classes.JSON import JSON
from classes.TSV import TSV
from classes.XML import XML


def test():
    csv_1 = CSV("resource/csv_data_1.csv")
    csv_1.read_data()
    csv_2 = CSV("resource/csv_data_2.csv")
    csv_2.read_data()
    json_1 = JSON("resource/json_data.json")
    json_1.read_data()
    xml_1 = XML("resource/xml_data.xml")
    xml_1.read_data()

    TSV.basic("resource/basic_results.tsv", csv_1, csv_2, json_1, xml_1)
    TSV.advanced("resource/advanced_results.tsv", csv_1, csv_2, json_1, xml_1)

    tsv_1 = TSV("resource/basic_results.tsv")
    tsv_1.read_data()

    tsv_2 = TSV("resource/advanced_results.tsv")
    tsv_2.read_data()

    ideal_tsv_1 = TSV("ideal/_basic_results.tsv")
    ideal_tsv_1.read_data()

    ideal_tsv_2 = TSV("ideal/_advanced_results.tsv")
    ideal_tsv_2.read_data()

    assert tsv_1 == ideal_tsv_1
    assert tsv_2 == ideal_tsv_2
