<template>
  <v-row justify="center" align="center" width=100%>
    <HomeHeader></HomeHeader>
    <div class="home-body">
      <v-img width=100%
        :src="'data:image/png;base64,'+imgData"
      >
      </v-img>
      <!-- <img v-bind:src="'data:image/png;base64,'+weatherImgData" /> -->
      <div class="img-bar">
        <HomeBody></HomeBody>
      </div>
      <!-- <div>{{ imgData }}</div> -->
    </div>
  </v-row>
</template>

<script>
import HomeHeader from '~/components/HomeHeader.vue'
import HomeBody from '~/components/HomeBody.vue'
import { mapState } from 'vuex'

export default {
  components: {
    HomeHeader,
    HomeBody,
  },
  data() {
    return{
    }
  },
  computed: {
    ...mapState('weather', ['imgData'])
  },
  mounted () {
  },
  methods: {
  }
}
</script>

<style scoped>
.home-body {
  position: relative;
}
.img-bar {
  position: absolute;
  top: 15%;
  left: 3%;
}
</style>
