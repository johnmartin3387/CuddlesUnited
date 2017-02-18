var MapsGoogle = function () {

    var mapBasic = function (focus_lat, focus_lng) {
        var map = new GMaps({
            div: '#gmap_basic',
            lat: focus_lat,
            lng: focus_lng
        });
        
        /*map.addMarker({
            lat: -51.38739,
            lng: -6.187181,
            title: 'Lima',
            details: {
                database_id: 42,
                author: 'HPNeo'
            },
            click: function (e) {
                if (console.log) console.log(e);
                alert('You clicked in this marker');
            }
        });*/ 
        
        map.setZoom(13);

        return map
    }
    return {
        //main function to initiate map samples
        init: function (focus_lat, focus_lng) {
            return mapBasic(focus_lat, focus_lng);
        }

    };

}();