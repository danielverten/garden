import pandas as pd
from flask import Flask, render_template, request
import time

veggie_db = pd.read_csv('/Users/daniel.verten/Desktop/wpp-python-web/FINAL_PROJECT/data/veggie_db.csv')
city_hardiness_zones = pd.read_csv('/Users/daniel.verten/Desktop/wpp-python-web/FINAL_PROJECT/data/city_hardiness_zones.csv')


def local_time():
    seconds = time.time()
    local_time = time.ctime(seconds)
    return local_time


app = Flask(__name__)


def get_city_list():
    city_df = pd.DataFrame(city_hardiness_zones)
    city_df_array = city_df.values
    city_dict = dict(city_df_array)
    city_list = list(sorted(city_dict.keys()))
    return city_list


def city_dictionary():
    city_df = pd.DataFrame(city_hardiness_zones)
    city_df_array = city_df.values
    city_dict = dict(city_df_array)
    return city_dict


def veggie_df():
    veggie_df = pd.DataFrame(veggie_db)
    return veggie_df


# def find_veggie_data(name, soil_difficulty, pest_difficulty, height, planting_distance, sowing_depth, diseases, pests, ph, sunshine):
#     veggie_dataf = veggie_df()
#     name_as_index = veggie_dataf.set_index("Name")
#     find_data_points = name_as_index.loc[name], [soil_difficulty, pest_difficulty, height, planting_distance, sowing_depth, diseases, pests, ph, sunshine]]
#     data_points = find_data_points.to_dict()
#     return data_points


def main():
    app.run(debug=True)


# select location, time of year and beginner/advanced grower
@app.route('/location', methods=['GET', 'POST'])
def location():
    city_list = get_city_list()
    return render_template("index.html", city_list=city_list)


# based on user input in /location, user sees some veggie options to grow, or can search for another vegetable
@app.route('/planner', methods=['GET', 'POST'])
def planner():
    city_dict = city_dictionary()
    veggie_dataframe = veggie_df()
    if request.method == 'POST':
        data = request.form
    # match passed on data to hardiness zone
    hardiness_zone = city_dict[data['city']]
    # filter vegie data based on hardiness hardiness zone
    sow_column_name = f"Zone {hardiness_zone} - Time to plant"
    filtered_veggie_data = veggie_dataframe[veggie_dataframe[sow_column_name].notna()]
    # display easy to plant veggies
    easy_to_is_true = filtered_veggie_data['Relative growing difficulty'] <= 2
    easy_to_grow_random = filtered_veggie_data[easy_to_is_true].sample(n=8)
    return render_template("planner.html", filtered_veggie_data=filtered_veggie_data, selected_city=data['city'], easy_to_grow_random=easy_to_grow_random)


@app.route('/veggies', methods=['GET', 'POST'])
def veggie_site():
    if request.method == 'POST':
        data = request.form
    veggie = data['veg']
    city = data['city']
    city_dict = city_dictionary()
    hardiness_zone = city_dict[data['city']]
    print(veggie)
    print(city)
    print(hardiness_zone)
    veggie_dataf = veggie_df()
    name_as_index = veggie_dataf.set_index("Name")
    find_data_points = name_as_index.loc[veggie]
    data_points = find_data_points.to_dict()
    print(data_points)
    # general data
    height = data_points['Height']
    distance = data_points['Planting distance']
    rel_diff = data_points['Relative growing difficulty']
    # soil data
    soil = data_points['Growing difficulty : Soil']
    soil_composition = data_points['Preferred soil type'].lower()[:-1]
    soil_ph = data_points['Soil PH'].lower()[:-1]
    soil_drain = data_points['Soil drainage'].lower()[:-1]
    # sow and harvest times
    sow = data_points[f'Zone {hardiness_zone} - Time to plant'][:-1]
    harvest = data_points[f'Zone {hardiness_zone} - Time to harvest'][:-1]
    care_diff = data_points['Care difficulty']
    # sun needed
    sun = data_points['Sunshine needed'].lower()[:-1]
    # pests and disease
    pests = data_points['Pests'].lower()[:-1]
    diseases = data_points['Plant diseases'].lower()[:-1]
    return render_template("veggies.html", city=city, veggie=veggie, soil=soil, soil_composition=soil_composition, soil_ph=soil_ph, height=height, distance=distance, sow=sow, harvest=harvest, sun=sun, soil_drain=soil_drain, care_diff=care_diff, pests=pests, rel_diff=rel_diff, diseases=diseases)


if __name__ == '__main__':
    main()
