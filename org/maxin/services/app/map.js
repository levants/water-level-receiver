function createMap (config) {
    function getDetails (id, callback) {
            /*
        var xhr = new XMLHttpRequest
        xhr.onreadystatechange = function () {
            if (xhr.status == xhr.DONE) {
                
            }
        }
        xhr.open('GET', 'get?id=' + id)
        xhr.send()
            */
        callback({
            id: id,
            desc: 1000
        })
    }
    function getNormalStyle () {
        return new ol.style.Style({
          image: new ol.style.Icon({
            anchor: [0.5, 48],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: 'app/icon.png'
          })
        })
	}
	
	function getSelectedStyle () {
        return new ol.style.Style({
          image: new ol.style.Icon({
            anchor: [0.5, 48],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: 'app/icon.png'
          })
        })
	}
	
    var view = new ol.View({
      center: ol.proj.fromLonLat([44, 42]),
      zoom: 8
    })
    
    var map = new ol.Map({
        target: config.target.id,
        layers: [new ol.layer.Tile({
            source: new ol.source.OSM()
        })],
        view: view
    })
    
    var layer = new ol.layer.Vector({
      source: new ol.source.Vector(),
      style: getNormalStyle()
    })
        
    map.addLayer(layer)

    var selectInteraction = new ol.interaction.Select();
    map.addInteraction(selectInteraction)

    selectInteraction.getFeatures().on('remove', function (e) {
        var feature = e.element
        feature.setStyle()
    })
    
    selectInteraction.getFeatures().on('add', function (e) {
        var selected = e.element
        var feature = selected.G
        
        //console.log(e.mapBrowserEvent.coordinate)
        
        if (feature.name == 'water-tank') {
            var data = feature.data
            selected.setStyle(getSelectedStyle())
            getDetails (data.id, function (details) {
                
                document.getElementById('item-id').innerHTML = 'ID: ' + details.id
                document.getElementById('item-desc').innerHTML =  'DESC: ' + details.desc
                
                popup.style.display = 'block'
            })
        }
    })
    
    var popup = document.getElementById('popup')
    var closer = document.getElementById('popup-closer')
    closer.onclick = function() {
        popup.style.display = 'none'
        closer.blur()
        return false
    }
    
    setTimeout(function () {
        config.getRandomPoints(function (points) {
            var features = []
            points.forEach(function (point) {
                features.push(createFeature('water-tank', point))
            })
            layer.getSource().clear()
            layer.getSource().addFeatures(features)
        })
    }, 10)
    
    function createFeature (name, data) {
        var f = new ol.Feature({
            name: name,
            data: data,
            geometry: new ol.geom.Point(ol.proj.fromLonLat([data.lon, data.lat]))
        })
        
        return f
    }
    
    return map
}
