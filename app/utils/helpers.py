def get_pokemon_data(data):
    pokemon_id = data.get("pokemon_id", None)
    pokemon_name = data.get("name", None)
    ability_list = [ability["ability"]["name"].title() for ability in data["abilities"]]
    type_list = [poke_type["type"]["name"].title() for poke_type in data["types"]]
    poke_data_dict = {
        "result": {
            "id": pokemon_id,
            "name": pokemon_name,
            "abilities": ability_list,
            "types": type_list,
            "poke_img": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
        }
    }
    return poke_data_dict
