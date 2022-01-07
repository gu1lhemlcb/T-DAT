<template>
  <div id="app" class="container">
    <h3>{{ user }}</h3>
    <h4>SalesMaille</h4>
    <JSCharting
      :options="chartOptionsSalesMaille"
      class="chartDiv"
    ></JSCharting>
    <h4>SalesFamille</h4>
    <JSCharting
      :options="chartOptionsSalesFamille"
      class="chartDiv"
    ></JSCharting>
    <h4>SalesMonth</h4>
    <JSCharting :options="chartOptionsSalesMonth" class="chartDiv"></JSCharting>
    <h4>SpentMonth</h4>

    <JSCharting :options="chartOptionsSpentMonth" class="chartDiv"></JSCharting>
    <h4>OrderMonth</h4>

    <JSCharting :options="chartOptionsOrderMonth" class="chartDiv"></JSCharting>
    <h4>CartMonth</h4>

    <JSCharting :options="chartOptionsCartMonth" class="chartDiv"></JSCharting>
    <h4>SalesFamilleMonth</h4>

    <JSCharting
      :options="chartOptionsSalesFamilleMonth"
      class="chartDiv"
    ></JSCharting>
    <h4>SalesMailleMonth</h4>

    <JSCharting
      :options="chartOptionsSalesMailleMonth"
      class="chartDiv"
    ></JSCharting>
    <h4>SpentFamilleMonth</h4>

    <JSCharting
      :options="chartOptionsSpentFamilleMonth"
      class="chartDiv"
    ></JSCharting>
    <h4>SpentMailleMonth</h4>

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
      chartOptionsSalesMaille: {
        type: "column",
        series: [
          {
            name: "SALES_PER_MAILLE",
            points: [],
          },
        ],
      },
      chartOptionsSalesFamille: {
        type: "column",
        series: [
          {
            name: "SALES_PER_FAMILLE",
            points: [],
          },
        ],
      },
      chartOptionsSalesMonth: {
        type: "line",
        series: [
          {
            name: "SALES_PER_MONTH",
            points: [],
          },
        ],
      },
      chartOptionsSpentMonth: {
        type: "line",
        series: [
          {
            name: "SPENT_PER_MONTH",
            points: [],
          },
        ],
      },
      chartOptionsOrderMonth: {
        type: "line",
        series: [
          {
            name: "ORDER_PER_MONTH",
            points: [],
          },
        ],
      },
      chartOptionsCartMonth: {
        type: "line",
        series: [
          {
            name: "AVERAGE_CART_PER_MONTH",
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