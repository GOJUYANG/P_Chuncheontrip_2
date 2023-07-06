import folium


parking = folium.features.CustomIcon(r'C:\Users\KDT104\Desktop\ChuncheonTrip\data_file\parking_lot_maps.png', icon_size=(30, 30))
world = folium.Map(zoom_start=2)
street_view = f'<a href="https://www.google.com/maps?layer=c&cbll={latitude},{longitude}">구글 거리뷰로 보기</a>'
popup = folium.Popup(street_view)
folium.Marker([33.3708091, 126.6935196],icon=parking,popup=popup).add_to(world)

world.show_in_browser()

