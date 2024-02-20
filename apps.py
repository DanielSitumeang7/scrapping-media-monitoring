from flask import Flask, request, jsonify, send_file, url_for, send_from_directory
from scrapping_models import scrape_bbc, scrapping_kompas, scrapping_tribune_two, scrapping_detikcom, total_halaman_scrapping_detikcom, total_halaman_scrapping_bbc, scrapping_liputanenam, total_halaman_cnn_indonesia, scrapping_cnn_indonesia, total_halaman_tribune, total_halaman_scrapping_kompas

from flask_cors import CORS  # Import the CORS module

app = Flask(__name__) # Membuat instance flask
CORS(app)  # Add CORS headers to the Flask app

@app.route('/scrapping-bbc', methods=['POST'])
def handle_scrapping_bbc():  # Changed function name to handle_scrapping_bbc
    if request.method == 'POST':
        query = request.form['kata_kunci']
        # output = scrape_bbc(query)
        total_halaman = total_halaman_scrapping_bbc(query)
        print(total_halaman)

        if total_halaman > 0:
            data = []
            for halaman in range(1,
            total_halaman+1):
                konten = scrape_bbc(query, halaman)
                if len(konten) > 0:
                    for i in konten:
                        print(i)
                        data.append(i)

            output = {
                "status" : "success",
                "status_code" : 200,
                "data" : data,
                "total_data" : len(data)
            }

        else:
            output = {
                "status" : "error",
                "status_code" : 404,
                "message" : "Data Tidak Ditemukan"
            }
    else:
        output = {
            "status" : "error",
            "status_code" : 400,
            "message" : "Method harus POST"
        }
    return jsonify(output)

@app.route('/scrapping-kompas', methods=['POST'])
def handle_scrapping_kompas():  # Changed function name to handle_scrapping_bbc
    if request.method == 'POST':
        query = request.form['kata_kunci']

        total_halaman = total_halaman_scrapping_kompas(query)

        if total_halaman > 0:

            data = []
            idkonten = 1
            for halaman in range(1,
            total_halaman+1):
                konten = scrapping_kompas(query, halaman)
                if len(konten) > 0:
                    for i in konten:
                        i['id'] = idkonten
                        data.append(i)

            output = {
                "status" : "success",
                "status_code" : 200,
                "data" : data,
                "total_data" : len(data)
            }
        else :
            output = {
                "status" : "error",
                "status_code" : 404,
                "message" : "Data Tidak Ditemukan"
            }
    else:

        output = {
            "status" : "error",
            "status_code" : 400,
            "message" : "Method harus POST"
        }
        
    return jsonify(output)

@app.route('/scrapping-tribune', methods=['POST'])
def handle_scrapping_tribune():
    if request.method == 'POST':
        query = request.form['kata_kunci']

        total_halaman = total_halaman_tribune(query)

        if total_halaman > 0:

            data = []
            idkonten = 1
            for halaman in range(1,
            total_halaman+1):
                konten = scrapping_tribune_two(query, halaman)
                if len(konten) > 0:
                    for i in konten:
                        i['id'] = idkonten
                        data.append(i)

            output = {
                "status" : "success",
                "status_code" : 200,
                "data" : data,
                "total_data" : len(data)
            }
    else:
        output = {
            "status" : "error",
            "status_code" : 400,
            "message" : "Method harus POST"
        }
    return jsonify(output)

@app.route('/scrapping-detikcom', methods=['POST'])
def handle_scrapping_detikcom():
    try :
        if request.method == 'POST':
            query = request.form['kata_kunci']
            total_halaman = total_halaman_scrapping_detikcom(query,1)
            if total_halaman > 0:
                data = []
                for halaman in range(1, total_halaman+1):
                    konten = scrapping_detikcom(query, halaman)
                    if len(konten) > 0:
                        for i in konten:
                            print(i)
                            data.append(i)

                output = {
                    "status" : "success",
                    "status_code" : 200,
                    "data" : data,
                    "total_data" : len(data)
                }
            else:
                output = {
                    "status" : "error",
                    "status_code" : 404,
                    "message" : "Data Tidak Ditemukan"
                }
        else:
            output = {
                "status" : "error",
                "status_code" : 400,
                "message" : "Method harus POST"
            }
        return jsonify(output)
    except Exception as e:
        return {
            "status" : "error",
            "status_code" : 500,
            "message" : str(e)
        }

@app.route('/scrapping-liputanenam', methods=['POST'])
def handle_scrapping_liputanenam():
    if request.method == 'POST':
        query = request.form['kata_kunci']
        data = scrapping_liputanenam(query)

        if len(data) > 0:
            output = {
                "status" : "success",
                "status_code" : 200,
                "data" : data,
                "total_data" : len(data)
            }

    else:
        output = {
            "status" : "error",
            "status_code" : 400,
            "message" : "Method harus POST"
        }

    return jsonify(output)

@app.route('/scrapping-cnn-indonesia', methods=['POST'])
def handle_scrapping_cnn_indonesia():
    if request.method == 'POST':
        query = request.form['kata_kunci']
        total_halaman = total_halaman_cnn_indonesia(query)
        print(total_halaman)

        if total_halaman > 0:
            data = []
            idkonten = 1
            for halaman in range(1,
            total_halaman+1):
                konten = scrapping_cnn_indonesia(query, halaman)
                if len(konten) > 0:
                    for i in konten:
                        i['id'] = idkonten
                        print(i)
                        data.append(i)
                        idkonten += 1

            output = {
                "status" : "success",
                "status_code" : 200,
                "data" : data,
                "total_data" : len(data)
            }

        else:
            output = {
                "status" : "error",
                "status_code" : 404,
                "message" : "Data Tidak Ditemukan"
            }
    else:
        output = {
            "status" : "error",
            "status_code" : 400,
            "message" : "Method harus POST"
        }
    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)