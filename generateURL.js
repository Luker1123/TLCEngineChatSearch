
// NOTES: 
// Add { "type": "module" } to package.json and change the name of the imported file 
// To run, execute "node generateURL" in a terminal
// String-type query parameters are case insensitive

import file from './Example5.json' assert { type : 'json' };
let URL = "https://krishnam.tlcengine.com/search/?orderby=newest&orderbydirection=DESC&page_number=1&searchmap=true&skip=0&view=maplist";

function JSON_to_URL() {

    for (let key in file) {

        try {

            switch (key) {

                case "acres":
                    if (file[key][0] != null) URL += "&acresmin=" + file[key][0];
                    if (file[key][1] != null) URL += "&acresmax=" + file[key][1];
                    break;
            
                case "city":
                    if (file[key] != null) URL += "&city=" + encodeURIComponent(file[key].trim());
                    break;

                case "homeFeatures":
                    for (let i in file[key]) URL += "&homeFeatures=" + encodeURIComponent(file[key][i].trim());
                    break;

                case "listingprice":
                    if (file[key][0] != null) URL += "&listingpricemin=" + file[key][0];
                    if (file[key][1] != null) URL += "&listingpricemax=" + file[key][1];
                    break;

                case "livingarea":
                    if (file[key][0] != null) URL += "&livingareamin=" + file[key][0];
                    if (file[key][1] != null) URL += "&livingareamax=" + file[key][1];
                    break;

                case "lotfeatures":
                    for (let i in file[key]) URL += "&lotfeatures=" + encodeURIComponent(file[key][i].trim());
                    break;

                case "propertystyle":
                    for (let i in file[key]) URL += "&propertystyle=" + encodeURIComponent(file[key][i].trim());
                    break;

                case "propertytype":
                    for (let i in file[key]) URL += "&propertytype=" + encodeURIComponent(file[key][i].trim());
                    break;

                case "stories":
                    if (file[key] != null) URL += "&stories=" + encodeURIComponent(file[key].trim());
                    break;

                case "streetaddress":
                    if (file[key] != null) URL += "&streetaddress=" + encodeURIComponent(file[key].trim());
                    break;

                case "yearbuilt":
                    if (file[key][0] != null) URL += "&yearbuiltmin=" + file[key][0];
                    if (file[key][1] != null) URL += "&yearbuiltmax=" + file[key][1];
                    break;

                default:
                    if (typeof(file[key]) == "string") file[key] = file[key].trim(); 
                    if (file[key] != null) URL += "&" + key + "=" + file[key];
                    break;
            }

        } catch (error) {
            console.error(key + " --> " + error);
        }
    }

    return URL;
}

console.log(JSON_to_URL());
