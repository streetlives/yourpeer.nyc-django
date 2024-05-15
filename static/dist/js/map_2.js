/*
Copyright (c) 2024 Streetlives, Inc.

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
*/

function mapInitContainer(){
  console.log('map init had init', window._hadMapInit)
  if(window._hadMapInit) return;

  window.addEventListener('popstate', function(event) {
    console.log('popstate fired!', event);
    this.location.reload();
  });

  let markers = [];
  let Marker, Mapp;
  const markerIcon =
    "data:image/svg+xml,%3Csvg width='25' height='32' viewBox='0 0 25 32' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg id='cash-pin' filter='url(%23filter0_d_28_9457)'%3E%3Cpath id='Shape' fill-rule='evenodd' clip-rule='evenodd' d='M12.5 1C16.6421 1 20 4.35786 20 8.5C20 11.907 14.926 19.857 13.125 22.572C12.9857 22.781 12.7512 22.9066 12.5 22.9066C12.2488 22.9066 12.0143 22.781 11.875 22.572C10.074 19.856 5 11.907 5 8.5C5 4.35786 8.35786 1 12.5 1Z' fill='%23FFDC00' stroke='%23323232' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/g%3E%3Cdefs%3E%3Cfilter id='filter0_d_28_9457' x='0.25' y='0.25' width='24.5' height='31.4066' filterUnits='userSpaceOnUse' color-interpolation-filters='sRGB'%3E%3CfeFlood flood-opacity='0' result='BackgroundImageFix'/%3E%3CfeColorMatrix in='SourceAlpha' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0' result='hardAlpha'/%3E%3CfeOffset dy='4'/%3E%3CfeGaussianBlur stdDeviation='2'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0'/%3E%3CfeBlend mode='normal' in2='BackgroundImageFix' result='effect1_dropShadow_28_9457'/%3E%3CfeBlend mode='normal' in='SourceGraphic' in2='effect1_dropShadow_28_9457' result='shape'/%3E%3C/filter%3E%3C/defs%3E%3C/svg%3E%0A";
  const myLocationIcon =
    "data:image/svg+xml,%3Csvg width='50' height='50' viewBox='0 0 50 50' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='25' cy='25' r='25' fill='%230085FF' fill-opacity='0.2'/%3E%3Ccircle cx='25' cy='25' r='7.5' fill='white'/%3E%3Ccircle cx='25' cy='25' r='5' fill='%230085FF'/%3E%3C/svg%3E ";
  const activeMarkerIcon =
    "data:image/svg+xml,%3Csvg width='34' height='45' viewBox='0 0 34 45' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg id='pin1' filter='url(%23filter0_d_28_9454)'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M17 1C23.6274 1 29 6.37258 29 13C29 18.4512 20.8816 31.1712 18 35.5152C17.7772 35.8497 17.4019 36.0506 17 36.0506C16.5981 36.0506 16.2228 35.8497 16 35.5152C13.1184 31.1696 5 18.4512 5 13C5 6.37258 10.3726 1 17 1Z' fill='%23323232'/%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M17 1C23.6274 1 29 6.37258 29 13C29 18.4512 20.8816 31.1712 18 35.5152C17.7772 35.8497 17.4019 36.0506 17 36.0506C16.5981 36.0506 16.2228 35.8497 16 35.5152C13.1184 31.1696 5 18.4512 5 13C5 6.37258 10.3726 1 17 1Z' stroke='%23323232' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/g%3E%3Cdefs%3E%3Cfilter id='filter0_d_28_9454' x='0.25' y='0.25' width='33.5' height='44.5506' filterUnits='userSpaceOnUse' color-interpolation-filters='sRGB'%3E%3CfeFlood flood-opacity='0' result='BackgroundImageFix'/%3E%3CfeColorMatrix in='SourceAlpha' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0' result='hardAlpha'/%3E%3CfeOffset dy='4'/%3E%3CfeGaussianBlur stdDeviation='2'/%3E%3CfeComposite in2='hardAlpha' operator='out'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0'/%3E%3CfeBlend mode='normal' in2='BackgroundImageFix' result='effect1_dropShadow_28_9454'/%3E%3CfeBlend mode='normal' in='SourceGraphic' in2='effect1_dropShadow_28_9454' result='shape'/%3E%3C/filter%3E%3C/defs%3E%3C/svg%3E%0A";
  const closedMarker =
    "data:image/svg+xml,%3Csvg width='25' height='32' viewBox='0 0 25 32' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg id='cash-pin' filter='url(%23filter0_d_28_9460)'%3E%3Cpath id='Shape' fill-rule='evenodd' clip-rule='evenodd' d='M12.5 1C16.6421 1 20 4.35786 20 8.5C20 11.907 14.926 19.857 13.125 22.572C12.9857 22.781 12.7512 22.9066 12.5 22.9066C12.2488 22.9066 12.0143 22.781 11.875 22.572C10.074 19.856 5 11.907 5 8.5C5 4.35786 8.35786 1 12.5 1Z' fill='%23F0F0F0' stroke='%23323232' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/g%3E%3Cdefs%3E%3Cfilter id='filter0_d_28_9460' x='0.25' y='0.25' width='24.5' height='31.4066' filterUnits='userSpaceOnUse' color-interpolation-filters='sRGB'%3E%3CfeFlood flood-opacity='0' result='BackgroundImageFix'/%3E%3CfeColorMatrix in='SourceAlpha' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0' result='hardAlpha'/%3E%3CfeOffset dy='4'/%3E%3CfeGaussianBlur stdDeviation='2'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0'/%3E%3CfeBlend mode='normal' in2='BackgroundImageFix' result='effect1_dropShadow_28_9460'/%3E%3CfeBlend mode='normal' in='SourceGraphic' in2='effect1_dropShadow_28_9460' result='shape'/%3E%3C/filter%3E%3C/defs%3E%3C/svg%3E%0A";

  const mapStyles = [
    {
      featureType: "administrative",
      elementType: "geometry",
      stylers: [
        {
          visibility: "off",
        },
      ],
    },
    {
      featureType: "administrative.land_parcel",
      elementType: "labels",
      stylers: [
        {
          visibility: "off",
        },
      ],
    },
    {
      featureType: "poi",
      stylers: [
        {
          visibility: "off",
        },
      ],
    },
    {
      featureType: "poi",
      elementType: "labels.text",
      stylers: [
        {
          visibility: "off",
        },
      ],
    },
    {
      featureType: "poi.park",
      stylers: [
        {
          saturation: -25,
        },
        {
          visibility: "on",
        },
      ],
    },
    {
      featureType: "road",
      elementType: "labels.icon",
      stylers: [
        {
          visibility: "off",
        },
      ],
    },
    {
      featureType: "road.highway",
      stylers: [
        {
          saturation: -25,
        },
      ],
    },
    {
      featureType: "road.local",
      elementType: "labels",
      stylers: [
        {
          visibility: "on",
        },
      ],
    },
    {
      featureType: "water",
      stylers: [
        {
          saturation: -45,
        },
      ],
    },
  ];

  let scale = 25;

  const centralPark = {
    lat: 40.782539,
    lng: -73.965602,
  };


  const centerMapBtn = document.getElementById('recenter-btn');
  let userLocation = null;

  centerMapBtn.addEventListener('click', centerTheMap)

  document.addEventListener('DOMContentLoaded', function() {
      if(window._hadMapInit) return;
      google.maps
      .importLibrary("maps")
      .then(() => {
        console.log("maps loaded");
        return google.maps.importLibrary("marker");
      })
      .then(() => {
        console.log("marker loaded");
        Marker = google.maps.Marker;
        Mapp = google.maps.Map;

      })
      .then(() => {
        initMap();
        if (typeof active_location == 'object') {
          initMiniMap({lat: active_location.lat, lng: active_location.lng})
          setUserPosition(false)
          switchActiveMarker(active_location.id)
          map?.panTo({lat: active_location.lat, lng: active_location.lng});
        } else {
          setUserPosition(true)
        }
      })
      .then(() => {
        fetchLocations()
        window._hadMapInit = true;
        

      })
      // .then(sortLocationsByGeo)
      .catch((e) => {
        console.log(e);
      });

  })


  async function getLocations() {
    try {
      let url = window.location.href;
      if(url.includes("?")) {
        url += "&json=true";
      } else {
        url += "?json=true";
      }
      const res = await axios.get(url);
      console.log(res)
      return res.data.locations;
    } catch(err) {
      console.log(err)
      return [];
    }
  }


  async function fetchLocations() {
    console.log('fetching locations')




    let map_locations = await getLocations();

    for (let i = 0; i < map_locations.length; i++) {
      for (let j = i + 1; j < map_locations.length; j++) {
        if (map_locations[i].lat === map_locations[j].lat && map_locations[i].lng === map_locations[j].lng) {
          const c = jitter(map_locations[j].lat, map_locations[j].lng, 0.003)
          map_locations[j].lat = c.lat;
          map_locations[j].lng = c.lng;
        }
      }
    }

    // console.log(map_locations);
  
    updatePins(map_locations);
  }

  window.fetchLocations = fetchLocations;


  function convertObjectToArray(inputObject) {
    const outputArray = [];

    for (const key in inputObject) {
      const openingHours = inputObject[key];
      const weekday = parseInt(key);

      const convertTime = (time) => {
        const [hour, minute] = time
          .replace(" AM", "")
          .replace(" PM", "")
          .split(":");
        let formattedHour = parseInt(hour);

        if (time.includes("PM") && formattedHour !== 12) {
          formattedHour += 12;
        }

        return `${formattedHour.toString().padStart(2, "0")}:${minute}:00`;
      };

      openingHours.forEach((hours) => {
        const convertedOpeningTime = convertTime(hours.opens_at);
        const convertedClosingTime = convertTime(hours.closes_at);
        outputArray.push({
          opens_at: convertedOpeningTime,
          closes_at: convertedClosingTime,
          weekday,
        });
      });
    }

    return outputArray.reverse();
  }

  function renderSchedule(schedule) {
    const weekdays = [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ];

    if (
      schedule.length === 7 &&
      schedule.every(
        (day) => day.opens_at === "00:00:00" && day.closes_at === "23:59:00"
      )
    ) {
      return "Open 24/7";
    }

    const dayNumberToName = (weekday) => weekdays[weekday - 1];

    const formatHour = (time) => {
      const regexMidnight = /(23:59:00)|(00:00:00)/;
      if (regexMidnight.test(time)) {
        return "midnight";
      }
      return moment(time, "HH:mm:ss").format("LT").replace(":00 ", " ");
    };

    const formatHours = (opens, closes) =>
      `${formatHour(opens)} to ${formatHour(closes)}`;

    const formatRange = ({ start, end }) => {
      if (end === start) {
        return dayNumberToName(start);
      }
      if (end === start + 1) {
        return `${dayNumberToName(start)} & ${dayNumberToName(end)}`;
      }
      return `${dayNumberToName(start)} to ${dayNumberToName(end)}`;
    };

    const orderedSchedule = _.orderBy(schedule, ["weekday", "opens_at"]);

    const daysGroupedByHours = orderedSchedule.reduce((grouped, day) => {
      const hoursString = formatHours(day.opens_at, day.closes_at);
      return {
        ...grouped,
        [hoursString]: [...(grouped[hoursString] || []), day.weekday],
      };
    }, {});

    const groupStrings = Object.keys(daysGroupedByHours).map((hoursString) => {
      const dayRanges = [];
      const remainingWeekdays = daysGroupedByHours[hoursString];

      while (remainingWeekdays.length) {
        const currentDayRange = dayRanges[dayRanges.length - 1];
        const day = remainingWeekdays.shift();

        if (currentDayRange && currentDayRange.end === day - 1) {
          currentDayRange.end = day;
        } else {
          dayRanges.push({ start: day, end: day });
        }
      }

      return `${dayRanges.map(formatRange).join(", ")} ${hoursString}`;
    });

    return `Open ${groupStrings.join(", ")}`;
  }



  async function createReportIssue(location_name, content, services) {
    console.log("reporing issue");
    

    const currentUrl = window.location.href;

    let text = `New error report for *${location_name}* \n${currentUrl} \n`;

    if (content.trim())
      text = `New error report for *${location_name}*\n${currentUrl} \n"_${content}_"\n`;

    if (services.length)
      text = `New error report for *${location_name}*\n${currentUrl} \n\n *Services:* \n-${services.join(
        "\n-"
      )} \n \n "_${content}_"\n`;

    return fetch("/report", {
      method: "post",
      headers: {
        Accept: "application/json, text/plain, */*",
      },
      body: JSON.stringify({ text }),
    });
  }

  function toL(text) {
    if(!text) return null;
    const normalizedString = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    // Convert the normalized string to lowercase
    return normalizedString.toLowerCase();
  }

  function paginate(items, pageNumber, pageSize) {
    const startIndex = (pageNumber - 1) * pageSize;

    return _(items).slice(startIndex).take(pageSize).value();
  }

  function triggerGtagEvent(location) {
    const services = [];
    const locationArea = `${location.name} ${location.area}`;

    if (location.accommodation_services.services.length) {
      services.push('Shelter & Housing');
    }
    if (location.clothing_services.services.length) {
      services.push('Clothing');
    }
    if (location.food_services.services.length) {
      services.push('Food');
    }
    if (location.health_services.services.length) {
      services.push('Health');
    }
    if (location.other_services.services.length) {
      services.push('Other Services');
    }
    if (location.personal_care_services.services.length) {
      services.push('Personal care');
    }

    

    if(window._paq) {
      window._paq.push(['trackEvent', 'Locations', 'Areas', locationArea]);
    }
    gtag('event', 'Areas', {
      'event_category' : 'Areas',
      'event_label': locationArea
    });

    services.forEach(function(service) {
      console.log('event')

      gtag('event','Area Services', {
        'event_category':'Area Services',
        'event_label':`${locationArea} - ${service}`
      });

      gtag('event', 'Services', {
        'event_category':'Services',
        'event_label':service
      });

      if(window._paq) {
        window._paq.push(['trackEvent', 'Locations', 'Area Services', `${locationArea} - ${service}`]);
        window._paq.push(['trackEvent', 'Locations', 'Services', service]);
      }
    });

  }



  let apikey = "AIzaSyAAPtKyMixw4dK4LIFDo9PwfsXgS0Xw8cw";
  let map, infoWindow, miniMap, panorama;


  function sortLocationsByServiceCount() {
    function compareServiceLength(obj1, obj2) {
      const length1 = Object.values(obj1)
        .filter((prop) => {
          return (
            typeof prop === "object" && !Array.isArray(prop) && prop !== null
          );
        })
        .filter((arr) => arr.services.length > 0).length;

      const length2 = Object.values(obj2)
        .filter(
          (prop) =>
            typeof prop === "object" && !Array.isArray(prop) && prop !== null
        )
        .filter((arr) => arr.services.length > 0).length;

      return length2 - length1; // Sort in descending order
    }

    // Sort the array of objects based on array lengths
    const sorted = locations.sort(compareServiceLength);
    Alpine.store("locations").locations = sorted;

    Alpine.store("locations").loading = false;
    updatePins(sorted);

    if (currentLocation) {
      switchActiveMarker(currentLocation);
      map.panTo({ lat: currentLocation.lat, lng: currentLocation.lng });
      map.setZoom(15);
      initMiniMap({ lat: currentLocation.lat, lng: currentLocation.lng });
    }

  }

  function getDirectionUrl(address) {
    const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(
      address
    )}`;

    return mapsUrl;

    // return `https://maps.google.com/maps?daddr=${encodeURIComponent(address)}`;
  }

  async function initMap() {
    console.log('doing initmap fn')
    infoWindow = new google.maps.InfoWindow();
    map = new Mapp(document.getElementById("map"), {
      center: centralPark,
      zoom: 14,
      streetViewControl: false,
      // gestureHandling: 'cooperative',
      mapTypeControl: false,
      fullscreenControl: false,
      styles: mapStyles,
    });
  }

  async function initMiniMap(center) {
    console.log('doing initminimap fn')

    if (Mapp) {
      window.minimap = new google.maps.Map(document.getElementById("miniMap"), {
        center: center,
        zoom: 17,
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: false,
        disableDefaultUI: true,
        styles: mapStyles,
      });

      const marker = new google.maps.Marker({
        position: center,
        map: window.minimap,
        title: "Location.",
        icon: markerIcon,
      });
    }
  }

  window.initMiniMap = initMiniMap;

  async function initMiniMap2(center) {
    console.log('doing initminimap2 fn')

    const minimap2 = new Mapp(document.getElementById("miniMap2"), {
      center: center,
      zoom: 15,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false,
      styles: mapStyles,
    });

    const marker = new google.maps.Marker({
      position: center,
      map: minimap2,
      title: "Location.",
      icon: markerIcon,
    });
  }


  function removeMarkers() {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null); // Remove marker from the map
    }
    markers = []; // Clear the markers array
  }

  function updatePins(locations) {

    if (!locations?.length) {
      removeMarkers();
      return;
    }

    // remove all the markers from the array and the map
    while (markers.length) {
      markers.pop().setMap(null);
    }

    // add the locations into the map
    for (let i = 0; i < locations.length; i++) {
      if (!locations[i].lat || !locations[i].lng) {
        continue;
      }
      let marker = new google.maps.Marker({
        position: {
          lat: locations[i].lat,
          lng: locations[i].lng,
        },
        lat: locations[i].lat,
        lng: locations[i].lng,
        map: map,
        closed: locations[i].closed,
        slug: locations[i].slug,
        id: locations[i].id,
        title: locations[i].name,
        icon: locations[i].closed ? closedMarker : markerIcon,
      });

      markers.push(marker);
      // if(markers.length === 1) {
      //   map.panTo({ lat: locations[i].lat, lng: locations[i].lng });
      // }
      marker.addListener("click", (e) => {

        const target = `/locations/${marker.slug}`;

        const pageWidth = document.documentElement.scrollWidth;

        if (pageWidth > 767) {
          window.location.href = target;
        } else {


        let hx_target = "#mobile_tray"
        let htmx_options = {target: hx_target, select:hx_target, swap: 'outerHTML'}
        console.log(marker.slug);

        htmx.ajax('GET', target, htmx_options).then(()=>
        {
           
          switchActiveMarker(marker.id)
          console.log('hello')
        })

  
        }


        


      });
    }

    scaleMap(markers);
  }

  function switchActiveMarker(id) {
    const markerToUpdate = markers.find((marker) => marker.id === id);

    if (!markerToUpdate) return;

    markers.forEach((m) => {
      if (m.icon == activeMarkerIcon)
        m.setIcon(m.closed ? closedMarker : markerIcon);
    });

    markerToUpdate.setIcon(activeMarkerIcon);
    map?.panTo(markerToUpdate.getPosition());
  }

  function removeActiveMarker() {
    markers.forEach((m) => {
      if (m.icon == activeMarkerIcon)
        m.setIcon(m.closed ? closedMarker : markerIcon);
    });
  }

  window.switchActiveMarker = switchActiveMarker;
  window.removeActiveMarker = removeActiveMarker;


  async function setUserPosition(center = true) {

    const mapScale = scale;

    window.navigator.geolocation.getCurrentPosition(
      (pos) => {
        const usl = {
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        };
        userLocation = usl;
        const marker = new google.maps.Marker({
          position: usl,
          map: map,
          title: "You are here!",
          icon: myLocationIcon,
        });

        const distance = calculateDistanceInMiles(
          usl.lat,
          usl.lng,
          40.782539,
          -73.965602
        );

        if (distance > 26) {

          if (center) map?.panTo(centralPark)

          userLocation = null;

        } else {
          if (center) map?.panTo(usl);
        }
      },
      () => {
          if (center) map?.panTo({
            lat: 40.782539,
            lng: -73.965602,
          });
          userLocation = null;
        console.log("geoloc err");
      }
    );
  }



  function scaleMap(markers) {
    console.log('scale map')
    if (!map) return;
  
    const list = markers;


    if (list.length === 1 && typeof active_location == 'object'){
      switchActiveMarker(list[0].id)
      map.panTo({ lat: list[0].lat, lng: list[0].lng });
      return;
    }

    let coordinates = []
  
  
    if (userLocation !== null) {
  

      const sortedByCenter = [...list].sort(function (a, b) {
        return calculateDistance(a, userLocation) - calculateDistance(b, userLocation);
      });

      coordinates = sortedByCenter.slice(0, 10);
      coordinates.push(userLocation)

  
    } else {
  
      const sortedByCenter = [...list].sort(function (a, b) {
        return calculateDistance(a, centralPark) - calculateDistance(b, centralPark);
      });

      coordinates = sortedByCenter.slice(0, 10);
      coordinates.push(userLocation)
    }

    var bounds = new google.maps.LatLngBounds();
    coordinates.forEach(function(coord) {
      var latLng = new google.maps.LatLng(coord.lat, coord.lng);
      bounds.extend(latLng);
    });

    map.fitBounds(bounds);
  
  }

  function centerTheMap() {


    let coordinates = markers.map(m => ({lat: m.lat, lng: m.lng}));
    
    if (userLocation) {

      coordinates = [...markers].sort(function (a, b) {
        return calculateDistance(a, userLocation) - calculateDistance(b, userLocation);
      }).slice(0, 10);

      coordinates.push(userLocation)
    } else {
      coordinates = [...markers].sort(function (a, b) {
        return calculateDistance(a, centralPark) - calculateDistance(b, centralPark);
      }).slice(0, 10);
      coordinates.push(centralPark)
    }

    var bounds = new google.maps.LatLngBounds();
    coordinates.forEach(function(coord) {
      var latLng = new google.maps.LatLng(coord.lat, coord.lng);
      bounds.extend(latLng);
    });

    map.fitBounds(bounds);

      
  }


  // Function to calculate distance between two points using Haversine formula
  function calculateDistanceInMiles(lat1, lng1, lat2, lng2) {
    const earthRadiusMiles = 3958.8; // Earth's radius in miles
    const dLat = toRad(lat2 - lat1);
    const dLng = toRad(lng2 - lng1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) *
        Math.cos(toRad(lat2)) *
        Math.sin(dLng / 2) *
        Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = earthRadiusMiles * c;

    return distance.toFixed(1);
  }

  function toRad(value) {
    return (value * Math.PI) / 180;
  }

  // Function to calculate the distance between two locations using Haversine formula
  function calculateDistance(userLocation1, userLocation2) {
    const radlat1 = (Math.PI * userLocation1.lat) / 180;
    const radlat2 = (Math.PI * userLocation2.lat) / 180;
    const theta = userLocation1.lng - userLocation2.lng;
    const radtheta = (Math.PI * theta) / 180;
    let dist =
      Math.sin(radlat1) * Math.sin(radlat2) +
      Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
    dist = Math.acos(dist);
    dist = (dist * 180) / Math.PI;
    dist = dist * 60 * 1.1515; // Distance in miles
    return dist;
  }



  function haversineDistance(point1, point2) {
    function toRad(value) {
      return (value * Math.PI) / 180;
    }

    var R = 6371; // Earth's radius in km
    var lat1 = point1.lat;
    var lon1 = point1.lng;
    var lat2 = point2.lat;
    var lon2 = point2.lng;

    var dLat = toRad(lat2 - lat1);
    var dLon = toRad(lon2 - lon1);

    var a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) *
        Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);

    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var distance = R * c;

    return distance;
  }



  let rad_Earth = 6378.16;
  let one_degree = (2 * Math.PI * rad_Earth) / 360;
  let one_km = 1 / one_degree;

  function randomInRange(from, to, fixed) {
    fixed = fixed || 10;
    return (Math.random() * (to - from) + from).toFixed(fixed) * 1;
  }

  function jitter(lat, lng, kms, fixed) {
    return {
      lat : randomInRange(
        lat - (kms * one_km),
        lat + (kms * one_km),
        fixed
      ),
      lng : randomInRange(
        lng - (kms * one_km),
        lng + (kms * one_km),
        fixed
      )
    };
  }

  function filterListing(thisElementId){
    let el = document.getElementById(thisElementId);

  }

}
mapInitContainer();
