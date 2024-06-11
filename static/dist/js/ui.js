/*
Copyright (c) 2024 Streetlives, Inc.

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
*/

function doSearch() {
    let input = document.getElementById('search_input').value
    let search_panel = document.getElementById('search_panel')
    let search_for = document.getElementById('search_for')
    let search_panel_link = document.getElementById('search_panel_link')
    let search_form = document.getElementById('search_form')

    if (input.length > 0) {
        search_panel.style.display = 'block'
        search_for.innerHTML = input
        search_panel_link.href = '/locations?search=' + input.split(' ').join('+')
        search_form.action = '/locations?search=' + input.split(' ').join('+')
        // set hx-get of search form
        search_form.setAttribute('hx-get', '/locations?search=' + input.split(' ').join('+'))

    } else {
        search_panel.style.display = 'none'
    }
}

function doSearchSubmit(event){
  event.preventDefault()
  let input = document.getElementById('search_input').value
  let search_form = document.getElementById('search_form')
  let search_panel = document.getElementById('search_panel')
  if (input.length > 0) {
    search_form.submit()
    // hide search panel
    search_panel.style.display = 'none'
  }
}

function sortQueryParams(url) {
    // Create a URL object
    let urlObj = new URL(url);

    // Get the query parameters
    let params = new URLSearchParams(urlObj.search);

    // Convert the parameters to an array of [key, value] pairs
    let paramsArray = Array.from(params.entries());

    // Sort the array by key and value
    paramsArray.sort((a, b) => {
        if (a[0] === b[0]) {
            return a[1] < b[1] ? -1 : 1;
        }
        return a[0] < b[0] ? -1 : 1;
    });

    // Create a new URLSearchParams object with the sorted parameters
    let sortedParams = new URLSearchParams(paramsArray);

    // Replace the original query parameters with the sorted parameters
    urlObj.search = sortedParams;

    // Return the new URL
    return urlObj.toString();
}

window._last_form_url = null;

function doFilterChange(key,value){
 // log doFilterchange 
  console.log('doFilterChange', key, value)
  let filter_form = document.getElementById('filters_form')
  let filter_shelter = document.getElementById('filter_shelter')
  let filter_food = document.getElementById('filter_food')
  let filter_clothing = document.getElementById('filter_clothing')
  let filter_personal_care = document.getElementById('filter_personal_care')
  let filter_health = document.getElementById('filter_health')
  let filter_other = document.getElementById('filter_other')
  let filter_shelter_value = filter_shelter.value
  let is_advanced_filters = document.getElementById('is_advanced_filters')
  let filter_open_now = document.getElementById('filter_open_now')
  let age_filter = document.getElementById('age_filter')
  let filter_not_open_now = document.getElementById('filter_not_open_now')
  let filter_shelter_type_any = document.getElementById('filter_shelter_type_any')
  let filter_shelter_type_single_adult = document.getElementById('filter_shelter_type_single_adult')
  let filter_shelter_type_families = document.getElementById('filter_shelter_type_families')
  let filter_food_type_any = document.getElementById('filter_food_type_any')
  let filter_food_type_soup_kitchen = document.getElementById('filter_food_type_soup_kitchen')
  let filter_food_type_food_pantry = document.getElementById('filter_food_type_food_pantry')
  let filter_clothing_type_any = document.getElementById('filter_clothing_type_any')
  let filter_clothing_type_casual = document.getElementById('filter_clothing_type_casual')
  let filter_clothing_type_professional = document.getElementById('filter_clothing_type_professional')
  let filter_personal_care_toiletries = document.getElementById('filter_personal_care_toiletries')
  let filter_personal_care_restrooms = document.getElementById('filter_personal_care_restrooms')
  let filter_personal_care_showers = document.getElementById('filter_personal_care_shower')
  let filter_personal_care_laundry = document.getElementById('filter_personal_care_laundry')
  let filter_personal_care_haircuts = document.getElementById('filter_personal_care_haircuts')
  let filter_requirement_types_referral_letter = document.getElementById('filter_requirement_types_referral_letter')
  let filter_requirement_types_any = document.getElementById('filter_requirement_types_any')
  let filter_requirement_types_registered_client = document.getElementById('filter_requirement_types_registered_client')

  let hx_target = "#filters_and_list_screen"
  let htmx_options = {target: hx_target, select:hx_target, headers:{'HX-Push-Url':'True'}}
  // reset all filters

  
  
  is_advanced_filters.value = 'true'



  let resetOpenNow = () => {
    filter_open_now.value = '';
    filter_not_open_now.value = '';
  }

  let resetShelterType = () => {
    filter_shelter_type_any.value = '';
    filter_shelter_type_single_adult.value = '';
    filter_shelter_type_families.value = '';
  }
  let resetFoodType = () => {
    filter_food_type_any.value = '';
    filter_food_type_soup_kitchen.value = '';
    filter_food_type_food_pantry.value = '';
  }
  let resetClothingType = () => {
    filter_clothing_type_any.value = '';
    filter_clothing_type_casual.value = '';
    filter_clothing_type_professional.value = '';
  }

  let resetPersonalCareType = () => {
    filter_personal_care_toiletries.value = '';
    filter_personal_care_restrooms.value = '';
    filter_personal_care_showers.value = '';
    filter_personal_care_laundry.value = '';
    filter_personal_care_haircuts.value = '';
    filter_personal_care_haircuts.checked = false;
    filter_personal_care_laundry.checked = false;
    filter_personal_care_showers.checked = false;
    filter_personal_care_restrooms.checked = false;
    filter_personal_care_toiletries.checked = false;

  }
  let resetRequirementTypes = () => {
    filter_requirement_types_any.checked = false;
    filter_requirement_types_referral_letter.checked = false;
    filter_requirement_types_registered_client.checked = false;
    filter_requirement_types_any.value = '';
    filter_requirement_types_referral_letter.value = '';
    filter_requirement_types_registered_client.value = '';
  }

  let resetAll = () => {
    resetClothingType();
    resetFoodType();
    resetShelterType();
    resetOpenNow();
    resetPersonalCareType();
    resetRequirementTypes();
    filter_shelter.value = '';
    filter_food.value = '';
    filter_clothing.value = '';
    filter_personal_care.value = '';
    filter_health.value = '';
    filter_other.value = '';
  }
  

  let getOptionalBaseUrl = () => {
    let base_url = window.location.href

    // remove open_now query
    let url = new URL(base_url);
    let params = new URLSearchParams(url.search);
    // perform a reset on all optional filters
    params.delete('open');
    params.delete('shelter');
    params.delete('food');
    params.delete('clothing');
    params.delete('requirement');
    params.delete('personal-care');
    params.delete('age');

    url.search = params.toString();
    url_string = url.toString()

    if (url_string.indexOf('?') == -1){
      return '?adv=yes'
    } else {
      if (url_string.indexOf('adv') == -1){
        return url_string + '&adv=yes'
      } else {
        return url_string
      }
    }
  }

  let getOpenNowQuery = () => {
    if(filter_open_now.value == 'true'){
      return '&open=yes'
    } else {
      return ''
    }
  }

  let getAgeQuery = () => {
    if(age_filter.value == ''){
      return ''
    } else {
      return '&age=' + age_filter.value
    }
  }

  let getShelterQuery = () => {
    let types = []
    if (filter_shelter_type_families.value == 'true'){
      types.push('family')
    } else if(filter_shelter_type_single_adult.value == 'true'){
      query = ''
      types.push('single')
    }
    if (types.length == 0){
      return ''
    }
    return "&shelter="+types.join('+')
  }

  let getFoodQuery = () => {
    let types = []
    if (filter_food_type_soup_kitchen.value == 'true'){
      types.push('kitchen')
    } else if (filter_food_type_food_pantry.value == 'true'){
      types.push('pantry')
    }
    if (types.length == 0){
      return ''
    }
    return "&food="+types.join('+')
  }

  let getClothingTypeQuery = () => {
    let types = []
     if (filter_clothing_type_casual.value == 'true'){
      types.push('casual')
    } else if (filter_clothing_type_professional.value == 'true'){
      types.push('professional')
    }
    if (types.length == 0){
      return ''
    }
    return "&clothing="+types.join('+')
  }

  let getRequirementsQuery = () => {
    let types = []
    // get what is checked
    let is_none = filter_requirement_types_any.checked
    let is_referral_letter = filter_requirement_types_referral_letter.checked
    let is_registered_client = filter_requirement_types_registered_client.checked
    if (is_none){
      types.push('no')
    }
    if (is_referral_letter){
      types.push('referral-letter')
    }
    if (is_registered_client){
      types.push('registered-client')
    }
    if (types.length == 0){
      return ''
    }
    return "&requirement="+types.join('+')
  }

  let getPersonalCareQuery = () => {
    let types = []
    let is_toiletries = filter_personal_care_toiletries.checked
    let is_restrooms = filter_personal_care_restrooms.checked
    let is_showers = filter_personal_care_showers.checked
    let is_laundry = filter_personal_care_laundry.checked
    let is_haircuts = filter_personal_care_haircuts.checked
    if (is_haircuts){
      types.push('haircut')
    }
    if (is_laundry){
      types.push('laundry')
    }
    if (is_restrooms){
      types.push('restrooms')
    }
    if (is_showers){
      types.push('showers')
    }
    if (is_toiletries){
      types.push('toiletries')
    }
    if (types.length == 0){
      return ''
    }
    return "&personal-care="+types.join('+')
    
    
    
    


    return query

  }

  let getHealthQuery = () => {
    let query = ''

    return query
  }

  let getOtherQuery = () => {
    let query = ''

    return query
  }

  function getQueryStringValue(url, key) {
    let params = (new URL(url)).searchParams;
    return params.get(key);
}

  let getPersonalCareUrl = ()=>{
    let urlObj = new URL(window.location.href);
    let baseUrl = urlObj.origin + "/personal-care";
    let optionals = getOptionalQueries()
    let personal_queries = getQueryStringValue(baseUrl + optionals, 'personal-care') || "";
    let personal_queries_array = personal_queries.split('+');
    let url = new URL(baseUrl);
    

    let types = []
    let is_toiletries = filter_personal_care_toiletries.checked
    let is_restrooms = filter_personal_care_restrooms.checked
    let is_showers = filter_personal_care_showers.checked
    let is_laundry = filter_personal_care_laundry.checked
    let is_haircuts = filter_personal_care_haircuts.checked
    let hadChange = false;


    if(is_laundry){
      baseUrl +="/laundry-services"
      hadChange = true;
    }
    if (is_haircuts){
      if(!hadChange){
        baseUrl += "/haircuts-barbers"
        hadChange = true;
      } else {
        types.push('haircuts')
      }
    }

    if (is_restrooms){
      if(!hadChange){
        baseUrl += "/restrooms"
        hadChange = true;
      } else {
        types.push('restrooms')
      }
    }
    if (is_showers){
      if(!hadChange){
        baseUrl += "/showers"
        hadChange = true;
      } else {
        types.push('showers')
      }
    }
    if (is_toiletries){
      if(!hadChange){
        baseUrl += "/toiletries"
        hadChange = true;
      } else {
        types.push('toiletries')
      }
    }

  
    if (types.length > 0){
      let url2 = new URL(baseUrl);
      let params2 = new URLSearchParams(window.location.href.search);
      params2.delete('personal-care')
      params2.append('personal-care', types.join('+'))
      params2.append('adv', 'yes')
      let newUrl = baseUrl +"?"+ params2.toString()
      newUrl = decodeURIComponent(newUrl)
      return sortQueryParams(newUrl)
    }

    let url2 = new URL(baseUrl);
    let params2 = new URLSearchParams(window.location.href.search);
    params2.delete('personal-care')
    params2.append('adv', 'yes')
    let newUrl = baseUrl +"?"+ params2.toString()
    newUrl = decodeURIComponent(newUrl)
    return sortQueryParams(newUrl)
  }


  let getOptionalQueries = () => {
    let queries = getOpenNowQuery() + getShelterQuery() + getFoodQuery() + getClothingTypeQuery() + getPersonalCareQuery() + getHealthQuery() + getOtherQuery() + getRequirementsQuery() + getAgeQuery()
    let base = "https://yourpeer.nyc/?adv=yes"
    queries = sortQueryParams(base+queries)
    return queries.replace(base, '')

  }

  // log all filter values



  if(key == 'shelter'){
    if(filter_shelter_value == 'true'){
      resetAll()
      htmx.ajax('GET', '/locations?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        console.log('in htmx locations callback')
        return fetchLocations()
      })
      
    } else {
      resetAll()        
      filter_shelter.value = 'true';
      htmx.ajax('GET', '/shelters-housing?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        console.log('in htmx shelters-housing callback')
        return fetchLocations()
      })
      
    }
  } else if (key == 'food') {
    if(filter_food.value == 'true'){
      resetAll()
      htmx.ajax('GET', '/locations?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    } else {
      resetAll()
      filter_food.value = 'true';
      htmx.ajax('GET', '/food?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    }
  } else if (key == 'clothing') {
    if(filter_clothing.value == 'true'){
      resetAll()
      htmx.ajax('GET', '/locations?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    } else {
      resetAll()
      filter_clothing.value = 'true';
      htmx.ajax('GET', '/clothing?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    }
  } else if (key == 'personal_care'){
    if(filter_personal_care.value == 'true'){
      resetAll()
      htmx.ajax('GET', '/locations?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    } else {
      resetAll()
      filter_personal_care.value = 'true';
      htmx.ajax('GET', '/personal-care?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    }
  } else if (key == 'health'){
    if(filter_health.value == 'true'){
      resetAll()
      htmx.ajax('GET', '/locations?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    } else {
      resetAll()
      filter_health.value = 'true';
      htmx.ajax('GET', '/health-care?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    }
  } else if (key == 'other'){
    if(filter_other.value == 'true'){
      resetAll()
      htmx.ajax('GET', '/locations?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    } else {
      resetAll()
      filter_other.value = 'true';
      htmx.ajax('GET', '/other-services?adv=yes' + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    }
  } else if (key == 'filters_popup'){
    if (value == 'open'){
      is_advanced_filters.value = 'true'
    }
    if (value == 'close'){
      is_advanced_filters.value = ''
      let url = new URL(window.location.href);
      let params = new URLSearchParams(url.search);
      params.delete('adv');
      url.search = params.toString();
      htmx.ajax('GET', url.toString(), htmx_options).then(()=>
      {
        return fetchLocations(url.toString())
      })
    }
  } else if(key == 'open_now'){
    if(filter_open_now.value == 'true'){
      resetOpenNow()
      htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    } else {
      resetOpenNow()
      filter_open_now.value = 'true';
      htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
    }
  } else if (key=='not_open_now'){
    resetOpenNow()
    let base_url = getOptionalBaseUrl()
    htmx.ajax('GET', base_url + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  
  } else if (key=='age_filter'){
    let base_url = getOptionalBaseUrl()
    htmx.ajax('GET', base_url + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  
  } else if (key == 'shelter_type_any'){
    resetShelterType()
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })

  } else if (key == 'shelter_type_single_adult'){
    resetShelterType()
    filter_shelter_type_single_adult.value = 'true';
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })

  } else if (key == 'shelter_type_families'){
    resetShelterType()
    filter_shelter_type_families.value = 'true';
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })

  } else if (key == 'food_type_any'){
    resetFoodType()
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })

  } else if (key == 'food_type_soup_kitchen') {
    resetFoodType()
    filter_food_type_soup_kitchen.value = 'true';
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })

  } else if (key == 'food_type_food_pantry') {
    resetFoodType()
    filter_food_type_food_pantry.value = 'true';
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'clothing_type_any'){
    resetClothingType()
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == "clothing_type_casual"){
    resetClothingType()
    filter_clothing_type_casual.value = 'true';
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == "clothing_type_professional"){
    resetClothingType()
    filter_clothing_type_professional.value = 'true';
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  
  } else if (key == 'requirement_types_any' || key == 'requirement_types_referral_letter' || key == 'requirement_types_registered_client'){
    htmx.ajax('GET', getOptionalBaseUrl() + getOptionalQueries(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'personal_care_toiletries'){
    htmx.ajax('GET', getPersonalCareUrl(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'personal_care_restrooms'){
    htmx.ajax('GET', getPersonalCareUrl(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'personal_care_showers'){
    htmx.ajax('GET', getPersonalCareUrl(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'personal_care_laundry'){
    htmx.ajax('GET', getPersonalCareUrl(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'personal_care_haircuts'){
    htmx.ajax('GET', getPersonalCareUrl(), htmx_options).then(()=>
      {
        return fetchLocations()
      })
  } else if (key == 'reset_filters'){
    resetAll()
    htmx.ajax('GET', '/locations', htmx_options).then(()=>
      {
        return fetchLocations()
      })
  }

  

}

function submitReportIssue(event) {
    event.preventDefault();
    // get all input fields with class .issue
    const checks = document.querySelectorAll(".issue");
    const currentUrl = window.location.href;
    let issues = currentUrl + "\n";
    for(let i = 0; i < checks.length; i++) {
      if(checks[i].checked) {
        issues += checks[i].value + "\n";
      }
    }
    issues += document.getElementById("reportContent").value;

    document.getElementById("reportView").style.display = "none";
    document.getElementById("reportCompletedView").style.display = "block";
    return fetch("/report", {
      method: "post",
      headers: {
        Accept: "application/json, text/plain, */*",
        'X-CSRFToken': document.getElementById('csrf_token').value,
      },
      body: issues,
    });
    


  }

  function succcessReportButton() {
    document.getElementById("reportContainer").style.display = "none";
    document.getElementById("locationDetailsContainer").style.display = "block";
  }

