const app = Vue.createApp({
    data: function () {
        return {
            categories: [],
            isWaitingForCategories: true,

            title: "",
            desc: "",
            category: "",
            amount: 0,

            submittedTitle: "",
            chance: 0,
            predictedAmount: 0,
            similar: [],

            isWaiting: true,
            status: ""
        };
    },
    methods: {
        sendRequest: function () {
            this.isWaiting = true;
            this.status = "Loading...";
            this.submittedTitle = this.title;
            
            input = {
                title: this.title,
                desc: this.desc,
                category: this.category,
                amount: this.amount
            }
            jsonString = JSON.stringify(input);

            var vue = this;
            fetch('https://kicksmarter.ue.r.appspot.com/api/idea', {
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
                vue.predictedAmount = data.amount;
                while (vue.similar.length > 0) {
                    vue.similar.pop();
                }
                for (var i in data.similar) {
                    vue.similar.push(data.similar[i]);
                }
                vue.isWaiting = false;
            })
            .catch(function(error) {
                vue.status = "Error :( Please try again!"
            });
        }
    }
}).mount("#app");

fetch('https://kicksmarter.ue.r.appspot.com/db/categories', {
    method: 'GET',
    headers: {'Content-Type': 'application/json'}
})
.then(function(response) {
    return response.json();
})
.then(function(data) {
    for (var i in data) {
        app.$data.categories.push(data[i]);
    }
    app.$data.category = data[0];
    app.$data.isWaitingForCategories = false;
})
.catch(function(error) {
    console.log(error);
});