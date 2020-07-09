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
    _tsv_1 = TSV("resource/basic_results.tsv")
    _tsv_1.read_data()
    _tsv_2 = TSV("resource/advanced_results.tsv")
    _tsv_2.read_data()

    CSV.basic("resource/basic_results.csv", csv_1, csv_2, json_1, xml_1)
    CSV.advanced("resource/advanced_results.csv", csv_1, csv_2, json_1, xml_1)
    _csv_1 = CSV("resource/basic_results.csv")
    _csv_1.read_data()
    _csv_2 = CSV("resource/advanced_results.csv")
    _csv_2.read_data()

    JSON.basic("resource/basic_results.json", csv_1, csv_2, json_1, xml_1)
    JSON.advanced("resource/advanced_results.json", csv_1, csv_2, json_1, xml_1)
    _json_1 = JSON("resource/basic_results.json")
    _json_1.read_data()
    _json_2 = JSON("resource/advanced_results.json")
    _json_2.read_data()

    XML.basic("resource/basic_results.xml", csv_1, csv_2, json_1, xml_1)
    XML.advanced("resource/advanced_results.xml", csv_1, csv_2, json_1, xml_1)
    _xml_1 = XML("resource/basic_results.xml")
    _xml_1.read_data()
    _xml_2 = XML("resource/advanced_results.xml")
    _xml_2.read_data()

    ideal_tsv_1 = TSV("ideal/_basic_results.tsv")
    ideal_tsv_1.read_data()
    ideal_tsv_2 = TSV("ideal/_advanced_results.tsv")
    ideal_tsv_2.read_data()

    print(_json_1)
    print(_xml_1)
    assert _tsv_1 == _csv_1 == _json_1 == _xml_1 == ideal_tsv_1
    assert _tsv_2 == _csv_2 == _json_2 == _xml_2 == ideal_tsv_2
