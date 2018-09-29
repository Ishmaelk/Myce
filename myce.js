
		let markers = [
				{
					coords:{lat: 40.714782, lng: -74.016018},
					//iconImage: ''
					content:'',
				},
				{
					coords:{lat: 40.714782, lng: -74.006018}
				},
				{
					coords:{lat: 40.712772, lng: -74.006058},
					content : 'i like apples',
				},
			]
		


		function initMap(){
			//map options
			let options = {
				zoom: 12,
				center: {lat: 40.712772, lng: -74.006058},
				styles: [
		            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
		            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
		            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
		            {
		              featureType: 'administrative.locality',
		              elementType: 'labels.text.fill',
		              stylers: [{color: '#d59563'}]
		            },
		            {
		              featureType: 'poi',
		              elementType: 'labels.text.fill',
		              stylers: [{color: '#d59563'}]
		            },
		            {
		              featureType: 'poi.park',
		              elementType: 'geometry',
		              stylers: [{color: '#263c3f'}]
		            },
		            {
		              featureType: 'poi.park',
		              elementType: 'labels.text.fill',
		              stylers: [{color: '#6b9a76'}]
		            },
		            {
		              featureType: 'road',
		              elementType: 'geometry',
		              stylers: [{color: '#38414e'}]
		            },
		            {
		              featureType: 'road',
		              elementType: 'geometry.stroke',
		              stylers: [{color: '#212a37'}]
		            },
		            {
		              featureType: 'road',
		              elementType: 'labels.text.fill',
		              stylers: [{color: '#9ca5b3'}]
		            },
		            {
		              featureType: 'road.highway',
		              elementType: 'geometry',
		              stylers: [{color: '#746855'}]
		            },
		            {
		              featureType: 'road.highway',
		              elementType: 'geometry.stroke',
		              stylers: [{color: '#1f2835'}]
		            },
		            {
		              featureType: 'road.highway',
		              elementType: 'labels.text.fill',
		              stylers: [{color: '#f3d19c'}]
		            },
		            {
		              featureType: 'transit',
		              elementType: 'geometry',
		              stylers: [{color: '#2f3948'}]
		            },
		            {
		              featureType: 'transit.station',
		              elementType: 'labels.text.fill', 
		              stylers: [{color: '#d59563'}]
		            },
		            {
		              featureType: 'water',
		              elementType: 'geometry',
		              stylers: [{color: '#17263c'}]
		            },
		            {
		              featureType: 'water',
		              elementType: 'labels.text.fill',
		              stylers: [{color: '#515c6d'}]
		            },
		            {
		              featureType: 'water',
		              elementType: 'labels.text.stroke',
		              stylers: [{color: '#17263c'}]
		            }
		          ]
			}
			// new map
			let map = new google.maps.Map(document.getElementById('map'), options)
			var heatMapData = [
			  {location: new google.maps.LatLng(40.712, -74.006), weight: 0.5},
			  new google.maps.LatLng(40.712, -122.445),
			  {location: new google.maps.LatLng(40.713, -74.005), weight: 2},
			  {location: new google.maps.LatLng(40.713, -74.004), weight: 3},
			  {location: new google.maps.LatLng(40.712, -74.003), weight: 2},
			  new google.maps.LatLng(40.712, -122.437),
			  {location: new google.maps.LatLng(40.712, -74.002), weight: 0.5},

			  {location: new google.maps.LatLng(40.712, -74.001), weight: 3},
			  {location: new google.maps.LatLng(40.714, -74.000), weight: 2},
			  new google.maps.LatLng(40.714, -122.443),
			  {location: new google.maps.LatLng(37.785, -74.003), weight: 0.5},
			  new google.maps.LatLng(40.712, -122.439),
			  {location: new google.maps.LatLng(40.713, -74.002), weight: 2},
			  {location: new google.maps.LatLng(40.717, -74.005), weight: 3}
			];
			var heatmap = new google.maps.visualization.HeatmapLayer({
			  data: heatMapData
			});
			heatmap.setMap(map);

			//add marker on click
			google.maps.event.addListener(map, 'click',
				function(event){
					addMarker({coords: event.latLng});
				});
			//array of markers
			
			//loop to display all the markers
			
				for(let i = 0; i < markers.length; i++){
					addMarker(markers[i]);
				}
			
		

			function addMarker(props){
				var marker = new google.maps.Marker({
				position: props.coords,
				map: map,
				//icon : ''
			});
				if(props.iconImage){
					marker.setIcon(props.iconImage);
				}
				if(props.content){
					let infoWindow = new google.maps.InfoWindow({
						content: props.content
					});

					marker.addListener('click', function(){
						infoWindow.open(map,marker)
					})
				}
			}
		}

		function formSubmit() {
			    var lat1, lng1;
			    lat1 = document.getElementById("lat").value;
			    lng1 = document.getElementById("lng").value;
			    markers.push({
						coords:{lat: parseFloat(lat1), lng: parseFloat(lng1)}
					})
			    initMap();
			}
		
		console.log(markers);
	