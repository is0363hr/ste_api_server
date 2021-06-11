const now = () => {
  const now = new Date()
  return now
}

const minute = () => {
  const now = new Date()
  const minute = Math.floor(now.getMinutes() / 5)*5
  return minute
}

const thumbTime = (year, month, day, hour, minute, timeVaule) => {
  var thumbTime = new Date(year, month, day, hour, minute)
  thumbTime.setMinutes(thumbTime.getMinutes() + timeVaule*5)
  const temMinutes = ("0" + thumbTime.getMinutes()).slice(-2)
  const temHours = ("0" + thumbTime.getHours()).slice(-2)
  const thumbTimeStr = temHours + ':' + temMinutes
  return thumbTimeStr
}

export default ({}, inject) => {
  inject('now', now)
  inject('minute', minute)
  inject('thumbTime', thumbTime)
}