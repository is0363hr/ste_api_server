// export const namespaced = true
import axios from '~/middleware/axios-weather-create'
// import fs from 'fs'
// import axios from 'axios'

export const state = () => ({
  imgYear: new Date().getFullYear(),
  imgMonth: new Date().getMonth()+1,
  imgDay: new Date().getDate(),
  imgHour: new Date().getHours(),
  imgMinute: Math.floor(new Date().getMinutes() / 5)*5,
  zoom: 4,
  lon: 135.000,
  lat: 34.000,
  imgPath: '/sye/4/img',
  imgData: "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",
})

export const mutations = {
  updateDateTime(state, dateTime) {
    state.imgYear = dateTime.imgYear,
    state.imgMonth = dateTime.imgMonth,
    state.imgDay = dateTime.imgDay,
    state.imgHour = dateTime.imgHour,
    state.imgMinute = dateTime.imgMinute
  },
  updateZoom(state, zoom) {
    state.zoom = zoom
  },
  updateCenterCoordinate(state, centerCoordinate) {
    state.lon = centerCoordinate.lon,
    state.lat = centerCoordinate.lat
  },
  updateImagePath(state, imgPath) {
    state.imgPath = imgPath
  },
  updateImageData(state, imgData) {
    state.imgData = imgData
  },
}

export const actions = {
  weatherImg({ commit, state }, requestData) {
    // commit('updateDateTime', requestData),
    axios
      .get(
        `/weather`,
        {
          params: {
            imgYear: requestData.imgYear,
            imgMonth: requestData.imgMonth,
            imgDay: requestData.imgDay,
            imgHour: requestData.imgHour,
            imgMinute: requestData.imgMinute,
            lon: requestData.lon,
            lat: requestData.lat,
            zoom: state.zoom,
          }
        })
      .then((response) => {
        commit('updateImageData', response.data)
        // console.log(response.data)
      })
      .catch(error=>{
        //失敗した時の処理
        console.log(error)
      })
  },
}

export const getters = {
  zoom(state) {
    return state.zoom
  },
  dateTime(state) {
    return [state.imgYear, state.imgMonth, state.imgDay, state.imgHour, state.imgMinute]
  },
  centerCoordinate(state) {
    return [state.lon, state.lat]
  },
  imgPath(state) {
    return state.imgPath
  },
  imgData(state) {
    return state.imgData
  },
}
