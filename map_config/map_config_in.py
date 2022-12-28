map_config_in = {'version': 'v1',
 'config': {'visState': {'filters': [{'dataId': ['all_data'],
     'id': 'dqm3foztf',
     'name': ['INB_DATE_TIME'],
     'type': 'timeRange',
     'value': [1651360620000, 1651446040000],
     'enlarged': True,
     'plotType': 'histogram',
     'animationWindow': 'free',
     'yAxis': None,
     'speed': 0.75}],
   'layers': [{'id': 'ko3a0p9',
     'type': 'arc',
     'config': {'dataId': 'all_data',
      'label': 'Flights_in',
      'color': [218, 112, 191],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat0': 'Lat_from',
       'lng0': 'Lon_from',
       'lat1': 'Lat_to',
       'lng1': 'Lon_to'},
      'isVisible': True,
      'visConfig': {'opacity': 0.8,
       'thickness': 3,
       'colorRange': {'name': 'Custom Palette',
        'type': 'custom',
        'category': 'Custom',
        'colors': ['#ff7f00',
         '#a6cee3',
         '#1f78b4',
         '#b2df8a',
         '#33a02c',
         '#fb9a99',
         '#e31a1c',
         '#B4CB8C',
         '#cab2d6',
         '#6a3d9a',
         '#ffff99',
         '#ADFF2F',
         '#00FF00',
         '#00FA9A',
         '#006400\t',
         '#66CDAA',
         '#FFE4B5',
         '#BDB76B',
         '#E6E6FA',
         '#D8BFD8',
         '#FF00FF',
         '#9370DB',
         '#8B008B',
         '#4B0082',
         '#000080',
         '#0000FF',
         '#1E90FF',
         '#B0E0E6\t',
         '#008080\t',
         '#556B2F',
         '#808000',
         '#9ACD32',
         '#2F4F4F',
         '#BC8F8F',
         '#A52A2A',
         '#BA55D3',
         '#2E8B57',
         '#FFD700',
         '#FFFF00',
         '#FFEFD5',
         '#00CED1',
         '#00CED1#2F4F4F',
         '#808080']},
       'sizeRange': [0, 10],
       'targetColor': None},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'Airline_Name',
       'type': 'string'},
      'colorScale': 'ordinal',
      'sizeField': None,
      'sizeScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'all_data': [{'name': 'AircraftType',
        'format': None},
       {'name': 'REG', 'format': None},
       {'name': 'INB_FLIGHT', 'format': None},
       {'name': 'INB_DATE_TIME', 'format': None},
       {'name': 'TOWN_FROM', 'format': None},
       {'name': 'COUNTRY', 'format': None}]},
     'compareMode': False,
     'compareType': 'absolute',
     'enabled': True},
    'brush': {'size': 0.5, 'enabled': False},
    'geocoder': {'enabled': False},
    'coordinate': {'enabled': False}},
   'layerBlending': 'normal',
   'splitMaps': [],
   'animationConfig': {'currentTime': None, 'speed': 1}},
  'mapState': {'bearing': 0,
   'dragRotate': False,
   'latitude': 41.657649375490124,
   'longitude': 89.14569946102559,
   'pitch': 0,
   'zoom': 2.0767292986029195,
   'isSplit': False},
  'mapStyle': {'styleType': 'm5bk6dm',    #'ini2ac'
   'topLayerGroups': {},
   'visibleLayerGroups': {'label': True,
    'road': True,
    'building': True,
    'water': True,
    'land': True},
   'threeDBuildingColor': [194.6103322548211,
    191.81688250953655,
    185.2988331038727],
   'mapStyles': {'m5bk6dm': {'accessToken': None,
     'custom': True,
     'icon': 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoidWNmLW1hcGJveCIsImEiOiJja3RpeXhkaXcxNzJtMnZxbmtkcnJuM3BkIn0.kGmGlkbuWaCBf7_RrZXULg&logo=false&attribution=false',
     'id': 'm5bk6dm',
     'label': 'Mapbox Streets',
     'url': 'mapbox://styles/mapbox/streets-v11'},
    'd65z8s4': {'accessToken': None,
     'custom': True,
     'icon': 'https://api.mapbox.com/styles/v1/mapbox/navigation-day-v1/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoidWNmLW1hcGJveCIsImEiOiJja3RpeXhkaXcxNzJtMnZxbmtkcnJuM3BkIn0.kGmGlkbuWaCBf7_RrZXULg&logo=false&attribution=false',
     'id': 'd65z8s4',
     'label': 'Mapbox Navigation Day',
     'url': 'mapbox://styles/mapbox/navigation-day-v1'},
    '9belde': {'accessToken': None,
     'custom': True,
     'icon': 'https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoidWNmLW1hcGJveCIsImEiOiJja3RpeXhkaXcxNzJtMnZxbmtkcnJuM3BkIn0.kGmGlkbuWaCBf7_RrZXULg&logo=false&attribution=false',
     'id': '9belde',
     'label': 'Mapbox Satellite Streets',
     'url': 'mapbox://styles/mapbox/satellite-streets-v11'},
    'ini2ac': {'accessToken': None,
     'custom': True,
     'icon': 'https://api.mapbox.com/styles/v1/mapbox/navigation-night-v1/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoidWNmLW1hcGJveCIsImEiOiJja3RpeXhkaXcxNzJtMnZxbmtkcnJuM3BkIn0.kGmGlkbuWaCBf7_RrZXULg&logo=false&attribution=false',
     'id': 'ini2ac',
     'label': 'Mapbox Navigation Night',
     'url': 'mapbox://styles/mapbox/navigation-night-v1'}}}}}