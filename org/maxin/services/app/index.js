(function () {
    var div = document.createElement('div')
    div.id = 'map'
    div.style.height = '100%'
    div.style.width = '100%'
    div.style.position = 'fixed'
    document.body.appendChild(div)
    createMap({
        target: div,
        getRandomPoints: getRandomPoints
    })
    
    
    function getRandomPoints (callback) {
        var n = 10 + random(10)
        var points = []
        for (var i = 0; i < n; i++) {
            points.push({
		id: i,
                lon: 42 + random(2) + random(10) * 0.01,
                lat: 42 + random(5) * 0.1 + random(10) * 0.01
            })
        }
        
        setTimeout(function () {
            callback(points)
        }, 0)
    }
    
    function random (n) {
        return Math.floor(Math.random() * (n + 1))
    }
})()
