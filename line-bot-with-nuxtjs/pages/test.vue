<template>
  <div class="container">
    <table border="1">
      <tbody>
      <tr>
        <th>ID</th>
        <th>画像名</th>
      </tr>
      <tr v-for="item in items" :key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.img_name }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: []
    }
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
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>