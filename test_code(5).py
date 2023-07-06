# 소스 코드 출처 : https://github.com/python-visualization/folium/issues/1344
# 소스 코드 출처 : https://stackoverflow.com/questions/37466683/create-a-legend-on-a-folium-map
# 소스 코드 출처 : https://stackoverflow.com/questions/76087520/how-to-make-a-python-folium-interactive-map-with-draggable-legend-and-clickable
# 소스 코드 출처 : https://developers.google.com/maps/documentation/javascript/adding-a-legend?hl=ko
# 소스 코드 출처 : https://stackoverflow.com/questions/65042654/how-to-add-categorical-legend-to-python-folium-map

#import folium
#
# # 범례에 대한 설명과 범례 아이콘 생성
# legend_html = '''
#      <div style="position: fixed;
#      bottom: 50px; left: 50px; width: 200px; height: 90px;
#      border:2px solid grey; z-index:9999; font-size:14px;
#      ">&nbsp; Legend <br>
#      &nbsp; Marker 1 <i class="fa fa-map-marker fa-2x"
#                   style="color:green"></i><br>
#      &nbsp; Marker 2 <i class="fa fa-map-marker fa-2x"
#                   style="color:blue"></i><br>
#       </div>
# '''
#
# # 맵 객체 생성
# m = folium.Map()
#
# # 맵 객체에 범례 추가
# m.get_root().html.add_child(folium.Element(legend_html))
#
# # 요소 추가
# folium.Marker(location=[37.5759, 126.9768],
#               icon=folium.Icon(color='green')).add_to(m)
#
# folium.Marker(location=[37.572007, 126.976653],
#               icon=folium.Icon(color='blue')).add_to(m)
#
# m.show_in_browser()

# import ee
# import geemap.foliumap as geemap
#
# Map = geemap.Map()
#
# landcover = ee.Image('MODIS/006/MCD12Q1/2013_01_01').select('LC_Type1')
# igbpLandCoverVis = {
#     'min': 1.0,
#     'max': 17.0,
#     'palette': [
#         '05450a',
#         '086a10',
#         '54a708',
#         '78d203',
#         '009900',
#         'c6b044',
#         'dcd159',
#         'dade48',
#         'fbff13',
#         'b6ff05',
#         '27ff87',
#         'c24f44',
#         'a5a5a5',
#         'ff6d4c',
#         '69fff8',
#         'f9ffa4',
#         '1c0dff',
#     ],
# }
#
# Map.setCenter(6.746, 46.529, 2)
# Map.addLayer(landcover, igbpLandCoverVis, 'MODIS Land Cover')
#
# Map.setCenter(6.746, 46.529, 2)
# Map.addLayer(landcover, igbpLandCoverVis, 'MODIS Land Cover')
# Map.add_legend(builtin_legend='MODIS/006/MCD12Q1')
#
#
# Map.add_legend(builtin_legend='NLCD')
#
# Map.addLayerControl()
#
# Map