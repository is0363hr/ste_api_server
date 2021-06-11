<template>
  <v-card width=100%>
    <v-list>
      <v-list-item>
        <v-icon large>mdi-weather-pouring</v-icon>
        <v-app-bar-title class=title>雨雲データ</v-app-bar-title>
        <v-card max-width=50%>
          <v-list-item>
            <v-select
              v-model="yearValue"
              :items="year"
              hint="年"
              persistent-hint
              @change="inputSelectTime"
            ></v-select>
            <v-select
              v-model="monthValue"
              :items="month"
              hint="月"
              persistent-hint
              @change="inputSelectTime"
            ></v-select>
            <v-select
              v-model="dayValue"
              :items="day"
              hint="日"
              persistent-hint
              @change="inputSelectTime"
            ></v-select>
            <v-select
              v-model="hourValue"
              :items="hour"
              hint="時"
              persistent-hint
              @change="inputSelectTime"
            ></v-select>
            <v-select
              v-model="minuteValue"
              :items="minute"
              hint="分"
              persistent-hint
              @change="inputSelectTime"
            ></v-select>
          </v-list-item>
        </v-card>
      </v-list-item>
    </v-list>
    <div class=timeBar>
      <v-slider
        v-model="timeValue"
        :color="color"
        :tick-labels="ticksLabels"
        thumb-label="always"
        step=1
        track-color="grey"
        ticks="always"
        always-dirty
        min="-36"
        max="12"
        @change="inputSliderTime"
      >
        <template v-slot:thumb-label>
          {{thumbTimeStr}}
        </template>
        <template v-slot:prepend>
          <v-icon
            large
            dark
            @click="decrement"
          >
            mdi-chevron-left-box
          </v-icon>
        </template>

        <template v-slot:append>
          <v-icon
            large
            dark
            @click="increment"
          >
            mdi-chevron-right-box
          </v-icon>
        </template>
      </v-slider>
    </div>
  </v-card>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'
export default {
  data () {
    return {
      timeValue: 0,
      interval: null,
      isPlaying: false,
      ticksLabels: [
          '-3時間',,,,,,,,,,,,
          '-2時間',,,,,,,,,,,,
          '-1時間',,,,,,,,,,,,
          '設定時間',,,,,,,,,,,,
          '+1時間',,,,,,,,,,,,
      ],

      yearValue: this.$now().getFullYear(),
      monthValue: this.$now().getMonth()+1,
      dayValue: this.$now().getDate(),
      hourValue: this.$now().getHours(),
      minuteValue: this.$minute(),
      year: [2021, 2020, 2019, 2018],
      month: [...Array(12).keys()].map(i => ++i),
      day: [...Array(31).keys()].map(i => ++i),
      hour: [...Array(24).keys()],
      minute: [...Array(12).keys()].map(i => i++*5),
      thumbTimeStr: this.$now().getHours() + ':' + this.$minute(),
    }
  },
  computed: {
    color () {
      if (this.timeValue < -23) return 'indigo'
      if (this.timeValue < -11) return 'teal'
      if (this.timeValue < 0) return 'green'
      if (this.timeValue < 1) return 'orange'
      return 'red'
    },
    animationDuration () {
      return `${12 / this.timeValue}s`
    },
  },
  methods: {
    ...mapMutations('weather', ['updateDateTime', 'updateCenterCoordinate']),
    ...mapActions('weather', ['weatherImg']),
    decrement () {
      this.timeValue--
      this.thumbTimeStr = this.$thumbTime(this.yearValue, this.monthValue, this.dayValue, this.hourValue, this.minuteValue, this.timeValue)
    },
    increment () {
      this.timeValue++
      this.thumbTimeStr = this.$thumbTime(this.yearValue, this.monthValue, this.dayValue, this.hourValue, this.minuteValue, this.timeValue)
    },
    toggle () {
      this.isPlaying = !this.isPlaying
    },
    inputSliderTime (){
      this.thumbTimeStr = this.$thumbTime(this.yearValue, this.monthValue, this.dayValue, this.hourValue, this.minuteValue, this.timeValue)
    },
    inputSelectTime (){
      this.timeValue = 0
      this.thumbTimeStr = this.$thumbTime(this.yearValue, this.monthValue, this.dayValue, this.hourValue, this.minuteValue, this.timeValue)
      this.weatherImg({
        imgYear: this.yearValue,
        imgMonth: this.monthValue,
        imgDay: this.dayValue,
        imgHour: this.hourValue,
        imgMinute: this.minuteValue,
        lon: 135.00,
        lat: 34.00
      })
    },
  },
}
</script>

<style scoped>
.title {
  margin: 2%;
}
.timeBar {
  margin: 3%;
}
</style>