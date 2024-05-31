
const app = Vue.createApp({
  delimiters:['[%','%]'],


    data() {
      return {
        message: 'Hello World!',

      }
    },
    methods: {
      
     async getMass(){
    

       const res = await axios.get("/api/resource/Teacher", { 'headers': { 'Authorization': AuthStr } });
       console.log(res);
      }
    },
  });
  app.mount('#app')




