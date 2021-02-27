const app = Vue.createApp({
    data: function () {
        return {
            five: 5
        };
    },
    methods: {
        sendRequest: function () {
            console.log('sending request');
            fetch('https://kicksmarter.ue.r.appspot.com/api', {
                method: 'POST',
                body: "{'title': 'adam has a cool title'}",
                headers:{'content-type': 'application/json'}
            })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    console.log(data);
                    console.log("chance: " + data.chance);
                    for (var i in data.similar) {
                        console.log("similar #" + i + " title: " + data.similar[i].title);
                        console.log("similar #" + i + " url: " + data.similar[i].url);
                    }
                });
        }
    }
}).mount("#app");