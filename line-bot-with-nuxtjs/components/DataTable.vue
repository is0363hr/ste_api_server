<template>
  <div id="app">
    <v-app id="inspire">
      <div>
        <v-data-table
          :headers="headers"
          :items="items"
          item-key="id"
          class="elevation-1"
          :search="search"
          :custom-filter="filterOnlyCapsText"
        >
          <template v-slot:top>
            <v-text-field
              v-model="search"
              label="Search (UPPER CASE ONLY)"
              class="mx-4"
            ></v-text-field>
          </template>
          <!-- <template v-slot:body.append>
            <tr>
              <td></td>
              <td>
                <v-text-field
                  v-model="calories"
                  type="number"
                  label="Less than"
                ></v-text-field>
              </td>
              <td colspan="4"></td>
            </tr>
          </template> -->
        </v-data-table>
      </div>
    </v-app>
  </div>
</template>

<script>
export default {
  data () {
    return {
      items: [],
      search: '',
      calories: '',
    }
  },
  computed: {
    headers () {
      return [
        {
          text: 'Id',
          align: 'start',
          sortable: false,
          value: 'id',
        },
        {
          text: 'ImageName',
          value: 'name',
          // filter: value => {
          //   if (!this.calories) return true

          //   return value < parseInt(this.calories)
          // },
        },
        // { text: 'Fat (g)', value: 'fat' },
        // { text: 'Carbs (g)', value: 'carbs' },
        // { text: 'Protein (g)', value: 'protein' },
        // { text: 'Iron (%)', value: 'iron' },
      ]
    },
  },
  methods: {
    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },
  },
  mounted: function() {
    this.$axios
      .$get('/api/database')
      .then(response => {
        this.items = response
      })
      .catch(error => {
        console.log(error)
      })
  },
}
</script>