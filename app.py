import os
import json
import quart
import quart_cors
from quart import request
from thoth import TarotReading  # Assuming this is the file where your TarotReading class is

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

tarot = TarotReading("data/thoth.json")

@app.post("/tarot")
async def get_tarot_reading():
    request_data = await request.get_json(force=True)
    num_cards = request_data.get('num_cards', 3)
    drawn_cards = tarot.draw_cards(num_cards)
    reading = tarot.read_cards(drawn_cards)
    return quart.Response(response=json.dumps(reading), status=200)

@app.post("/tarot_search/name")
async def search_tarot_name():
    request_data = await request.get_json(force=True)
    query = request_data.get('query', '')
    search_result = tarot.search_by_name(query)
    return quart.Response(response=json.dumps(search_result), status=200)

@app.post("/tarot_search/interpretation")
async def search_tarot_interpretation():
    request_data = await request.get_json(force=True)
    query = request_data.get('query', '')
    search_result = tarot.search_by_interpretation(query)
    return quart.Response(response=json.dumps(search_result), status=200)

@app.post("/tarot_search/attributes")
async def search_tarot_attributes():
    request_data = await request.get_json(force=True)
    query = request_data.get('query', '')
    search_result = tarot.search_by_attributes(query)
    return quart.Response(response=json.dumps(search_result), status=200)

@app.post("/tarot_search/all")
async def search_tarot_all():
    request_data = await request.get_json(force=True)
    query = request_data.get('query', '')
    search_result = tarot.search_all_fields(query)
    return quart.Response(response=json.dumps(search_result), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
