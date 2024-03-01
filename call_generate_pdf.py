import pathlib, json
from energy_pdf.create_document import EnergyPdfGenerator

if __name__ == "__main__":
    import time
    import os


    start = time.time()
    with open(pathlib.Path(__file__).parent / "limeon_invoice_sample.json") as file:
        invoice_data = json.load(file)

    client_data = {'client_name': 'test',
                   'codice_cliente': 'test',
                   'codice_fiscale': 'test',
                   'codice_destinatario': 'test',
                   'letter2': 'test',
                   'offerta': 'test',
                   'codice_offerta': 'test',
                   'codice_pod': 'test',
                   'tipologia': 'test',
                   'contratto': 'test', }
    energy_pdf_generator = EnergyPdfGenerator(invoice_data, "it", client_data)

    invoice_folder, invoice_filepath = energy_pdf_generator.generate_pdf()
    print('#' * 50)
    print(f"ukupno vreme: {time.time() - start}")
    print('#' * 50)
    with open(invoice_filepath, "rb") as file:
        content = file.read()

    import shutil

    shutil.rmtree(invoice_folder)
