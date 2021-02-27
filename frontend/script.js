const app = Vue.createApp({
    data: function () {
        return {
            title: "adam has a cooler title",
            desc: "",
            category: "",
            amount: 0,

            chance: 0,
            similar: []
        };
    },
    methods: {
        sendRequest: function () {
            console.log('sending request');
            input = {
                title: this.title,
                desc: this.desc,
                category: this.category,
                amount: this.amount
            }
            jsonString = JSON.stringify(input);

            var vue = this;
            setTimeout(function() {
                fetch('https://kicksmarter.ue.r.appspot.com/api', {
                    method: 'POST',
                    body: jsonString,
                    headers: {'Content-Type': 'application/json'}
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    console.log(data);
                    vue.chance = data.chance;
                    while (vue.similar.length > 0) {
                        vue.similar.pop();
                    }
                    for (var i in data.similar) {
                        vue.similar.push(data.similar[i]);
                    }
                });
            }, 2000);
        }
    }
}).mount("#app");