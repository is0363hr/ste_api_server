import colors from 'vuetify/es5/util/colors'

const { LINE_CHANNEL_ID } = process.env.LINE_CHANNEL_ID
const { LINE_CHANNEL_SECRET } = process.env.LINE_CHANNEL_SECRET
const { RASPBERRYPI_URL } = process.env.RASPBERRYPI_URL
const { BASE_LOCAL_TEST_URL } = process.env.BASE_LOCAL_TEST_URL
const { LOCAL_URL } = process.env.LOCAL_URL
const { MYSQL_HOST_ADDRESS } = process.env.MYSQL_HOST_ADDRESS

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - line-bot-with-nuxtjs',
    title: 'line-bot-with-nuxtjs',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/utils'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/dotenv',
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
  ],

  serverMiddleware: [
    { path: "/", handler: "~/server/index.js" },
  ],

  axios: {
    proxy: true
  },

  proxy: {
    '/api/weather': {
        target: `${process.env.RASPBERRYPI_URL}/api`,
        pathRewrite: {
            '^/api/weather': '/'
        },
        // target: `${process.env.BASE_LOCAL_TEST_URL}/api`,
        // pathRewrite: {
        //     '^/api': '/'
        // },
    }
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  mode: "universal",

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    extend (config, ctx) {
      config.node = {
        fs: "empty"
      }
    }
  },
  env: {
    LINE_CHANNEL_ID,
    LINE_CHANNEL_SECRET,
    RASPBERRYPI_URL,
    BASE_LOCAL_TEST_URL,
    LOCAL_URL,
    MYSQL_HOST_ADDRESS,
  },
}
