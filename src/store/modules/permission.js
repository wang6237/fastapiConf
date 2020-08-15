import { asyncRoutes, constantRoutes } from '@/router'
import {getMenu} from "@/api/user";
import Layout from '@/layout'
/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}


export function generaMenu(routes, data) {
  data.forEach(item => {
    console.log(0,item)
    // alert(JSON.stringify(item))
    let component
    if (item.layout) {
      component = Layout
    } else {
      component = (resolve) => require([`@/views${item.url}/index.vue`], resolve)
    }
    const menu = {
      path: item.url === '#' ? item.menu_id + '_key' : item.url,
      component: component ,
      // component: () => import(`@/views${item.url}/index`),
      // component: item.url === '#' ? Layout : () => import(`@/views${item.url}/index`),
      // hidden: true,
      children: [],
      name: 'menu_' + item.menu_id,
      meta: { title: item.menu_name, id: item.menu_id, roles: ['admin'] }
    }
    console.log(1,routes)
    if (item.children) {
      generaMenu(menu.children, item.children)
    }
    console.log(3, menu)
    routes.push(menu)
  })
}



/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      const loadMenuData = []
      getMenu().then(response => {
        console.log(response.data.menuList)
        let data = response
        // let data
        if (response.data.state !== 0) {
          console.log('菜单数据加载异常')
          // this.$message({
          //   message: '菜单数据加载异常',
          //   type: 0
          // })
        } else {
          data = response.data.menuList
          Object.assign(loadMenuData, data)
          // console.log(d)
          generaMenu(asyncRoutes, loadMenuData)
          let accessedRoutes
          if (roles.includes('admin')) {
            // alert(JSON.stringify(asyncRoutes))
            accessedRoutes = asyncRoutes || []
          } else {
            accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
          }
          commit('SET_ROUTES', accessedRoutes)
          resolve(accessedRoutes)
        }
        //generaMenu(asyncRoutes, data)
      }).catch(error => {
        console.log(error)
      })

      // let accessedRoutes
      // if (roles.includes('admin')) {
      //   accessedRoutes = asyncRoutes || []
      //   console.log(1, asyncRoutes)
      // } else {
      //   accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
      // }
      // commit('SET_ROUTES', accessedRoutes)
      // resolve(accessedRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
