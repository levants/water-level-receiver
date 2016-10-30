(function() {
    var div = document.createElement('div')
    div.id = 'map'
    div.style.height = '100%'
    div.style.width = '100%'
    div.style.position = 'fixed'
    document.body.appendChild(div)
    createMap({
        target : div,
        getRandomPoints : getRandomPoints
    })

    function getRandomPoints(callback) {

        var xhr = new XMLHttpRequest()
        xhr.open('GET', '/?containers=true', true)
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var container_records = JSON.parse(xhr.responseText)
                var points = []
                var cont_record
                for (var i = 0; i < container_records.length; i++) {
                    cont_record = JSON.parse(container_records[i])
                    console.log(cont_record)
                    points.push({
                        id : cont_record.container_id,
                        lon : cont_record.container_coordinates.long_val,
                        lat : cont_record.container_coordinates.lat_val
                    })
                    console.log(points)
                }

                setTimeout(function() {
                    callback(points)
                }, 0)
            }
        }
        xhr.send(null)

        // var n = 10 + random(10)
        // var points = []
        // for (var i = 0; i < n; i++) {
        // points.push({
        // id : i,
        // lon : 42 + random(2) + random(10) * 0.01,
        // lat : 42 + random(5) * 0.1 + random(10) * 0.01
        // })
        //
        // console.log(points)
        // }
        //
        // setTimeout(function() {
        // callback(points)
        // }, 0)
    }

    function random(n) {
        return Math.floor(Math.random() * (n + 1))
    }
})()
