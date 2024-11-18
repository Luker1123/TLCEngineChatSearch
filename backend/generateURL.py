import json
import urllib.parse

# Base URL
# Shold put this in the .env
url = "https://krishnam.tlcengine.com/search/?orderby=newest&orderbydirection=DESC&page_number=1&searchmap=true&skip=0&view=maplist"


def json_to_url(data):
    global url
    for key, value in data.items():
        try:
            if key == "acres":
                if value[0] is not None:
                    url += f"&acresmin={value[0]}"
                if value[1] is not None:
                    url += f"&acresmax={value[1]}"
            elif key == "city":
                if value:
                    url += f"&city={urllib.parse.quote(value.strip())}"
            elif key == "homeFeatures":
                for feature in value:
                    url += f"&homeFeatures={urllib.parse.quote(feature.strip())}"
            elif key == "listingprice":
                if value[0] is not None:
                    url += f"&listingpricemin={value[0]}"
                if value[1] is not None:
                    url += f"&listingpricemax={value[1]}"
            elif key == "livingarea":
                if value[0] is not None:
                    url += f"&livingareamin={value[0]}"
                if value[1] is not None:
                    url += f"&livingareamax={value[1]}"
            elif key == "lotfeatures":
                for feature in value:
                    url += f"&lotfeatures={urllib.parse.quote(feature.strip())}"
            elif key == "propertystyle":
                for style in value:
                    url += f"&propertystyle={urllib.parse.quote(style.strip())}"
            elif key == "propertytype":
                for ptype in value:
                    url += f"&propertytype={urllib.parse.quote(ptype.strip())}"
            elif key == "stories":
                if value:
                    url += f"&stories={urllib.parse.quote(value.strip())}"
            elif key == "streetaddress":
                if value:
                    url += f"&streetaddress={urllib.parse.quote(value.strip())}"
            elif key == "yearbuilt":
                if value[0] is not None:
                    url += f"&yearbuiltmin={value[0]}"
                if value[1] is not None:
                    url += f"&yearbuiltmax={value[1]}"
            else:
                if isinstance(value, str):
                    value = value.strip()
                if value is not None:
                    url += f"&{key}={value}"
        except Exception as error:
            print(f"{key} --> {error}")
    return url

# Test Code
# with open("test.json", "r") as file:
#    data = json.load(file)
#final_url = json_to_url(data)
# print(final_url)
