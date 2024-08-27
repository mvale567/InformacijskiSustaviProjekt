from flask import Flask, request, make_response, jsonify, render_template
from pony import orm

DB = orm.Database()

app = Flask(__name__)


# entiteti
class Bicikl(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    proizvodac = orm.Required(str)
    model = orm.Required(str)
    velicina = orm.Required(str)
    tezina = orm.Required(float)
    broj_brzina = orm.Required(int)
    vrsta_namjene = orm.Required(str)
    godina_proizvodnje = orm.Required(int)
    cijena = orm.Required(float)
    opis = orm.Required(str)

# sql baza - povezivanje
DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


def add_bicikl(json_request):
    try:

        proizvodac = json_request["proizvodac"]
        model = json_request["model"]
        velicina = json_request["velicina"]
        tezina = float(json_request["tezina"])
        broj_brzina = int(json_request["broj_brzina"])
        vrsta_namjene = json_request["vrsta_namjene"]
        godina_proizvodnje = int(json_request["godina_proizvodnje"])
        cijena = float(json_request["cijena"])
        opis = json_request["opis"]

        # spremanje u bazu
        with orm.db_session:
            Bicikl(proizvodac=proizvodac, model=model, velicina=velicina, tezina=tezina,
                   broj_brzina=broj_brzina, vrsta_namjene=vrsta_namjene, godina_proizvodnje=godina_proizvodnje,
                   cijena=cijena, opis=opis)
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

# dohvacanje svih podataka iz baze
def get_bicikli():
    try:
        with orm.db_session:
            db_query = orm.select(b for b in Bicikl)[:]
            results_list = [b.to_dict() for b in db_query]
            response = {"response": "Success", "data": results_list}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

#brisanje_bicikla
def delete_bicikl(bicikl_id):
    try:
        with orm.db_session:
            to_delete = Bicikl[bicikl_id]
            to_delete.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}



def patch_bicikl(bicikl_id, json_request):
    try:
        with orm.db_session:
            to_update = Bicikl[bicikl_id]

            if 'proizvodac' in json_request:
                to_update.proizvodac = json_request['proizvodac']
            if 'model' in json_request:
                to_update.model = json_request['model']
            if 'velicina' in json_request:
                to_update.velicina = json_request['velicina']
            if 'tezina' in json_request:
                to_update.tezina = float(json_request['tezina'])
            if 'broj_brzina' in json_request:
                to_update.broj_brzina = int(json_request['broj_brzina'])
            if 'vrsta_namjene' in json_request:
                to_update.vrsta_namjene = json_request['vrsta_namjene']
            if 'godina_proizvodnje' in json_request:
                to_update.godina_proizvodnje = int(json_request['godina_proizvodnje'])
            if 'cijena' in json_request:
                to_update.cijena = float(json_request['cijena'])
            if 'opis' in json_request:
                to_update.opis = json_request['opis']

            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
def get_bicikl_by_id(bicikl_id):
    try:
        with orm.db_session:
            bicikl = Bicikl[bicikl_id]
            if bicikl:
                response = {"response": "Success", "data": bicikl.to_dict()}
                return response
            else:
                return {"response": "Fail", "error": "Bicikl not found"}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

# add_item.html
@app.route("/dodaj/bicikl", methods=["POST", "GET"])
def dodaj_bicikl():
    if request.method == "POST":
        try:
            if request.is_json:
                json_request = request.get_json()
                app.logger.debug(f"Primljen JSON zahtjev: {json_request}")
            else:
                json_request = {}
                for key, value in request.form.items():
                    json_request[key] = value if value else None
                app.logger.debug(f"Primljen FORM zahtjev: {json_request}")

            required_keys = [
                "proizvodac", "model", "velicina", "tezina", "broj_brzina", "vrsta_namjene",
                "godina_proizvodnje", "cijena", "opis"
            ]

            for key in required_keys:
                if key not in json_request:
                    app.logger.error(f"Nedostaje ključ: {key}")
                    return make_response(jsonify({"response": "Fail", "error": f"Missing key: {key}"}), 400)

            # pretvaranje podataka iz forme
            json_request["tezina"] = float(json_request["tezina"])
            json_request["broj_brzina"] = int(json_request["broj_brzina"])
            json_request["godina_proizvodnje"] = int(json_request["godina_proizvodnje"])
            json_request["cijena"] = float(json_request["cijena"])

            response = add_bicikl(json_request)

            if response["response"] == "Success":
                app.logger.debug("Bicikl uspješno dodan.")
                return make_response(render_template("warehouse/add_item.html"), 200)
            else:
                app.logger.error(f"Greška prilikom dodavanja bicikla: {response['error']}")
                return make_response(jsonify(response), 400)

        except Exception as e:
            app.logger.exception("Greška prilikom obrade zahtjeva:")
            return make_response(jsonify({"response": "Fail", "error": str(e)}), 400)
    else:
        return make_response(render_template("warehouse/add_item.html"), 200)

@app.route("/vrati/bicikle", methods=["GET"])
def vrati_bicikle():
    if 'id' in request.args:
        bicikl_id = int(request.args.get("id"))
        response = get_bicikl_by_id(bicikl_id)
        if response["response"] == "Success":
            return make_response(render_template("warehouse/warehouse-home.html", bicikli=[response["data"]]), 200)
        return make_response(jsonify(response), 400)
    
    response = get_bicikli()
    if response["response"] == "Success":
        return make_response(render_template("warehouse/warehouse-home.html", bicikli=response["data"]), 200)
    return make_response(jsonify(response), 400)

# edit.html
@app.route("/vrati/bicikle/edit", methods=["GET"])
def vrati_bicikle_edit():
    if 'id' in request.args:
        bicikl_id = int(request.args.get("id"))
        response = get_bicikl_by_id(bicikl_id)
        if response["response"] == "Success":
            return make_response(render_template("warehouse/edit.html", bicikli=[response["data"]]), 200)
        return make_response(jsonify(response), 400)
    
    response = get_bicikli()
    if response["response"] == "Success":
        return make_response(render_template("warehouse/edit.html", bicikli=response["data"]), 200)
    return make_response(jsonify(response), 400)

# Rukovanje zahtjevima za brisanje bicikla prema ID-u
@app.route("/bicikli/<int:bicikl_id>", methods=["DELETE"])
def obrisi_bicikl(bicikl_id):
    response = delete_bicikl(bicikl_id)
    if response["response"] == "Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)

@app.route("/bicikli/<int:bicikl_id>", methods=["PATCH"])
def izmjeni_bicikl(bicikl_id):
    try:
        # Provjerava Content-Type ispravnosti
        if request.content_type != 'application/json':
            return make_response(jsonify({"response": "Fail", "error": "Content-Type must be application/json"}), 400)

        # Pokušaj preuzimanja JSON tijela zahtjeva
        json_request = request.get_json()

        if json_request is None:
            return make_response(jsonify({"response": "Fail", "error": "Missing or invalid JSON body"}), 400)

        response = patch_bicikl(bicikl_id, json_request)

        if response.get("response") == "Success":
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify(response), 400)

    except Exception as e:
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 500)


@app.route("/bicikl/<int:bicikl_id>", methods=["GET"])
def get_bicikl(bicikl_id):
    response = get_bicikl_by_id(bicikl_id)
    if response["response"] == "Success":
        return jsonify(response["data"])
    return jsonify(response), 400

# Ovaj dio je povezan sa vizualizacija.html, i on dohvaca podatke get_bicikli()
@app.route('/vizualizacija')
def vizualizacija():
    try:
        response = get_bicikli()
        if response["response"] == "Success":
            bicikli = response["data"]
            app.logger.debug(f"Podaci o biciklima: {bicikli}")
            return render_template("warehouse/vizualizacija.html", bicikli=bicikli)
        else:
            app.logger.error(f"Greška pri dobivanju bicikala: {response}")
            return make_response(jsonify(response), 400)
    except Exception as e:
        app.logger.exception("Greška prilikom obrade vizualizacije:")
        return make_response(jsonify({"response": "Fail", "error": str(e)}), 500)

# Dodani dijelovi kako bih mogao otvarati ostale html tagove kroz Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/warehouse')
def warehouse():
    return render_template('warehouse.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Naredba s kojom se pokrece aplikacija
if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)
