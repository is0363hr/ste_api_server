<template>
  <v-card>
    <div class=timeBar>
      <v-slider
        v-model="zoom"
        thumb-label="true"
        thumb-size="45"
        step=1
        track-color="grey"
        ticks="always"
        always-dirty
        min="4"
        max="14"
        vertical
      >
        <template v-slot:thumb-label="{ value }">
          zoom{{ value }}
        </template>
        <template v-slot:prepend>
          <v-icon
            large
            dark
            @click="decrement"
          >
            mdi-minus
          </v-icon>
        </template>

        <template v-slot:append>
          <v-icon
            large
            dark
            @click="increment"
          >
            mdi-plus
          </v-icon>
        </template>
      </v-slider>
    </div>
  </v-card>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  data () {
    return {
      zoom: 4,
      interval: null,
      isPlaying: false,
    }
  },
  computed: {
  },
  methods: {
    ...mapMutations('weather', ['updateZoom']),
    decrement () {
      this.zoom--
      this.updateZoom(this.zoom)
    },
    increment () {
      this.zoom++
      this.updateZoom(this.zoom)
    },
    toggle () {
      this.isPlaying = !this.isPlaying
    },
  },
}
</script>

<style scoped>
.timeBar {
  margin: 5%;
}
</style>