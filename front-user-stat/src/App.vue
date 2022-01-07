<template>
  <div id="app" class="container">
    <h1>Client: {{ user }}</h1>
    
    <h3>Nb de commande total: {{ totalStats.totalOrder }}</h3>
    <h4>Nb de commande par MOIS</h4>
    <JSCharting :options="chartOptionsOrderMonth" class="chartDiv"></JSCharting>

    <h3>Nb d'articles achetés total: {{ totalStats.articleSold }}</h3>
    <h4>Nb d'articles achetés total par MOIS</h4>
    <JSCharting :options="chartOptionsSalesMonth" class="chartDiv"></JSCharting>
    
    <h4>Nb d'articles achetés total par FAMILLE</h4>
    <JSCharting
      :options="chartOptionsSalesFamille"
      class="chartDiv"
    ></JSCharting>

    <h4>Nb d'd'articles achetés total par FAMILLE par MOIS</h4>
    <JSCharting
      :options="chartOptionsSalesFamilleMonth"
      class="chartDiv"
    ></JSCharting>
    
    <h4>Nb d'articles achetés total par MAILLE</h4>
    <JSCharting
      :options="chartOptionsSalesMaille"
      class="chartDiv"
    ></JSCharting>
    
    <h4>Nb d'd'articles achetés par MAILLE par MOIS</h4>
    <JSCharting
      :options="chartOptionsSalesMailleMonth"
      class="chartDiv"
    ></JSCharting>
    

    <h3>Prix du panier moyen: {{ totalStats.averageCart }}€</h3>
      
    <h4>Prix du panier moyen par MOIS</h4>
    <JSCharting :options="chartOptionsCartMonth" class="chartDiv"></JSCharting>
    
    <h3>Dépenses totales: {{ totalStats.totalSpent }}€</h3>
        
    <h4>Dépenses moyennes par MOIS</h4>
    <JSCharting :options="chartOptionsSpentMonth" class="chartDiv"></JSCharting>
      
    <h4>Dépenses totales par FAMILLE par MOIS</h4>
    <JSCharting
      :options="chartOptionsSpentFamilleMonth"
      class="chartDiv"
    ></JSCharting>
    
    <h4>Dépenses totales par MAILLE par MOIS</h4>
    <JSCharting
      :options="chartOptionsSpentMailleMonth"
      class="chartDiv"
    ></JSCharting>
  </div>
</template>

<script>
import JSCharting from "jscharting-vue";
import axios from "axios";

export default {
  name: "App",
  components: {
    JSCharting,
  },
  data() {
    return {
      user: 0,
      totalStats: {
        totalSpent: 0,
        articleSold: 0,
        totalOrder: 0,
        averageCart: 0,
      },
      chartOptionsSalesMaille: {
        type: "column",
        series: [
          {
            name: "d'articles achetés par MAILLE",
            points: [],
          },
        ],
      },
      chartOptionsSalesFamille: {
        type: "column",
        series: [
          {
            name: "d'articles achetés par FAMILLE",
            points: [],
          },
        ],
      },
      chartOptionsSalesMonth: {
        type: "line",
        series: [
          {
            name: "d'articles achetés pas MOIS",
            points: [],
          },
        ],
      },
      chartOptionsSpentMonth: {
        type: "line",
        series: [
          {
            name: "Dépenses par MOIS",
            points: [],
          },
        ],
      },
      chartOptionsOrderMonth: {
        type: "line",
        series: [
          {
            name: "Commandes par MOIS",
            points: [],
          },
        ],
      },
      chartOptionsCartMonth: {
        type: "line",
        series: [
          {
            name: "Panier par MOIS",
            points: [],
          },
        ],
      },
      chartOptionsSpentMailleMonth: {
        //SPENT_PER_MAILLE_PER_MONTH
        type: "column",
        series: [],
      },
      chartOptionsSpentFamilleMonth: {
        //SPENT_PER_FAMILLE_PER_MONTH
        type: "column",
        series: [],
      },
      chartOptionsSalesMailleMonth: {
        //SALES_PER_MAILLE_PER_MONTH
        type: "column",
        series: [],
      },
      chartOptionsSalesFamilleMonth: {
        //SALES_PER_FAMILLE_PER_MONTH
        type: "column",
        series: [],
      },
    };
  },

  mounted() {
    axios
      .get("stats.json")
      .then((response) => {
        this.user = response.data.user;
        this.totalStats.averageCart = response.data.stats["AVERAGE_CART"].data;
        this.totalStats.totalOrder = response.data.stats["TOTAL_ORDER"].data;
        this.totalStats.articleSold = response.data.stats["ARTICLES_SOLD"].data;
        this.totalStats.totalSpent = response.data.stats["TOTAL_SPENT"].data;

        //
        //  SALES_PER_MAILLE
        //
        let tmp = response.data.stats["SALES_PER_MAILLE"].data;
        for (const property in tmp) {
          this.chartOptionsSalesMaille.series[0].points.push({
            x: property,
            y: tmp[property],
          });
        }

        //
        //  SALES_PER_FAMILLE
        //
        tmp = response.data.stats["SALES_PER_FAMILLE"].data;
        for (const property in tmp) {
          this.chartOptionsSalesFamille.series[0].points.push({
            x: property,
            y: tmp[property],
          });
        }

        //
        //  SALES_PER_MONTH
        //
        tmp = response.data.stats["SALES_PER_MONTH"].data;
        for (const property in tmp) {
          this.chartOptionsSalesMonth.series[0].points.push({
            x: property,
            y: tmp[property],
          });
        }
        //
        //  SPENT_PER_MONTH
        //
        tmp = response.data.stats["SPENT_PER_MONTH"].data;
        for (const property in tmp) {
          this.chartOptionsSpentMonth.series[0].points.push({
            x: property,
            y: tmp[property],
          });
        }

        //
        //  ORDER_PER_MONTH
        //
        tmp = response.data.stats["ORDER_PER_MONTH"].data;
        for (const property in tmp) {
          this.chartOptionsOrderMonth.series[0].points.push({
            x: property,
            y: tmp[property],
          });
        }

        //
        //  AVERAGE_CART_PER_MONTH
        //
        tmp = response.data.stats["AVERAGE_CART_PER_MONTH"].data;
        for (const property in tmp) {
          this.chartOptionsCartMonth.series[0].points.push({
            x: property,
            y: tmp[property],
          });
        }

        //
        //  SPENT_PER_MAILLE_PER_MONTH
        //
        tmp = response.data.stats["SPENT_PER_MAILLE_PER_MONTH"].data;
        for (const property in tmp) {
          let tmp2 = [];
          for (let property2 in tmp[property]) {
            tmp2.push({
              x: property2,
              y: tmp[property][property2],
            });
          }
          this.chartOptionsSpentMailleMonth.series.push({
            name: property,
            points: tmp2,
          });
        }
        //
        //  SPENT_PER_FAMILLE_PER_MONTH
        //
        tmp = response.data.stats["SPENT_PER_FAMILLE_PER_MONTH"].data;
        for (const property in tmp) {
          let tmp2 = [];
          for (let property2 in tmp[property]) {
            tmp2.push({
              x: property2,
              y: tmp[property][property2],
            });
          }
          this.chartOptionsSpentFamilleMonth.series.push({
            name: property,
            points: tmp2,
          });
        }
        //
        //  SALES_PER_MAILLE_PER_MONTH
        //
        tmp = response.data.stats["SALES_PER_MAILLE_PER_MONTH"].data;
        for (const property in tmp) {
          let tmp2 = [];
          for (let property2 in tmp[property]) {
            tmp2.push({
              x: property2,
              y: tmp[property][property2],
            });
          }
          this.chartOptionsSalesMailleMonth.series.push({
            name: property,
            points: tmp2,
          });
        }
        //
        //  SALES_PER_FAMILLE_PER_MONTH
        //
        tmp = response.data.stats["SALES_PER_FAMILLE_PER_MONTH"].data;
        for (const property in tmp) {
          let tmp2 = [];
          for (let property2 in tmp[property]) {
            tmp2.push({
              x: property2,
              y: tmp[property][property2],
            });
          }
          this.chartOptionsSalesFamilleMonth.series.push({
            name: property,
            points: tmp2,
          });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>