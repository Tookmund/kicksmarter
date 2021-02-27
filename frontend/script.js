const app = Vue.createApp({
    data: function () {
        return {
            title: "",
            desc: "",
            category: "",
            amount: 0,

            chance: 0,
            similar: [],

            isWaiting: true,
            hasSubmitted: false // becomes and stays true upon clicking submit for first time
        };
    },
    methods: {
        sendRequest: function () {
            this.isWaiting = true;
            this.hasSubmitted = true;
            
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
                    vue.isWaiting = false;
                });
            }, 2000);
        }
    }
}).mount("#app");