import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import ToastService from '@/plugins/toasts';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    redirect: '/pages/home'
                },
                {
                    path: '/pages/test',
                    name: 'test',
                    component: () => import('@/views/pages/TestPage.vue')
                },
                {
                    path: '/pages/home',
                    name: 'homepage',
                    component: () => import('@/views/pages/Homepage.vue')
                },
                {
                    path: '/pages/released-assistance',
                    name: 'released assistance',
                    component: () => import('@/views/pages/ReleasedAssistance.vue')
                }
            ]
        },
        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        }
    ]
});

router.beforeEach((to, from, next) => {
   
    if (to.name === 'login' && localStorage.getItem('token')) {
        next({ name: 'homepage' });
    } else if (to.name !== 'login' && !localStorage.getItem('token')) {
        next({ name: 'login' });
    } else {
        next();
    }
})

export default router;
