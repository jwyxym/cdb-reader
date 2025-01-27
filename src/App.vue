<template>
    <div class = "main_page">
        <div id = "main_page_left">
            <transition name = "slide_list_page">
                <list_page v-if = "main_page.show_list.card" @event_close_cdb = " main_page.remove" @event_unshow_list_page = "whether_show_list_page" :cdb = "send_props.list_page.cdb" :selected = "send_props.list_page.select"/>
            </transition>
            <transition name = "under_list_page">
                <div v-if = "main_page.show_list.cdb" id = "under_list_page">
                    <div id = "upload_area" @dragenter.prevent="main_page.uploading = true" @dragover.prevent="main_page.uploading = true" @dragleave.prevent="main_page.uploading = false" @drop.prevent="upload_file.drag" @click="() => { upload_file_input.click(); }">
                        <h4>拖拽文件或点击此处上传文件</h4>
                        <input type = "file" multiple accept="image/*, text/*, .lua, .cdb, .ypk, .zip, .tar, .tgz, .tar.gz, .7z, .rar" ref = "upload_file_input" @change = "upload_file.click" style = "display: none;"/>
                    </div>
                    <div id = "cdb_list">
                        <button v-for="(i, v) in (main_page.page.count[0] > 0? Array(main_page.cdb.content.length >= main_page.page.count[0] * 10? 10 : main_page.cdb.content.length % 10) : [])" :key="v" @click = "whether_show_list_page(v)">{{ main_page.cdb.content[v + (Math.abs(main_page.page.count[0]) - 1) * 10] }}</button>
                    </div>
                    <div class = "cdb_list_btn">
                        <button @click = "main_page.page.previous"
                            :style = "{ 'background-color': main_page.page.count[0] <= 1 ? 'gray' : 'green', 'color': main_page.page.count[0] <= 1 ? 'black' : 'white' }"
                        >上一页</button>
                        <span>第<input @input = "filter_input($event)" v-model = "main_page.page.count[0]"/>页<br>共{{ Math.ceil(main_page.cdb.content.length / 10) }}页</span>
                        <button @click = "main_page.page.next"
                            :style = "{ 'background-color': main_page.page.count[0] >= Math.ceil(main_page.cdb.content.length / 10) ? 'gray' : 'green', 'color': main_page.page.count[0] >= Math.ceil(main_page.cdb.content.length / 10) ? 'black' : 'white' }"
                        >下一页</button>
                    </div>
                </div>
            </transition>
        </div>
        <card_page :pic = "send_props.card_page.pic" :close = "send_props.card_page.close" :cdb = "send_props.card_page.cdb" @event_close_fixed = "() => { send_props.card_page.close = '' }" @event_change_menu = "main_page.cdb.get_new"/>
    </div>
</template>

<script setup lang = "ts">
    import list_page from './components/list.vue'
    import card_page from './components/card.vue'

    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';
import { send } from 'vite';

    let send_props = reactive({
        card_page: {
            cdb: '',
            pic: '',
            close: ''
        },
        list_page: {
            cdb: ['暂未打开cdb'],
            select : new Map().set('cdb', '').set('page', -1).set('card', -1).set('entrust', false)
        }
    });

    let main_page = reactive({
        page : {
            count : [0],
            next : function () {
                if (main_page.page.count[0] < Math.ceil(main_page.cdb.content.length / 10))
                    main_page.page.count[0] ++ ;
            } as () => void,
            previous : function () {
                if (main_page.page.count[0] > 1)
                    main_page.page.count[0] -- ;
            } as () => void
        },
        cdb : {
            content : [] as string[],
            get :  async function (v) {
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/get_cdb_menu', {
                        cdb: ( typeof v === 'number' ? main_page.cdb.content[v + (Math.abs(main_page.page.count[0]) - 1) * 10] : v)
                    });
                    send_props.list_page.cdb = response.data;
                    send_props.card_page.cdb = response.data[0][0];
                } catch (error) {}
            } as (v : string | number) => Promise<void>,
            get_new : async function (v, id) {
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/get_cdb_menu', {
                        cdb: ( typeof v === 'number' ? main_page.cdb.content[v + (Math.abs(main_page.page.count[0]) - 1) * 10] : v)
                    });
                    let c = -1;
                    let p = 1;
                    for (let i = 0; i < response.data.length; i++) {
                        if (response.data[i].includes(id)) {
                            p = i;
                            c = response.data[i].indexOf(id);
                            break;
                        }
                    }
                    send_props.list_page.select.set('page', p);
                    send_props.list_page.select.set('card', c);
                    send_props.list_page.select.set('entrust', true);
                    send_props.list_page.cdb = response.data;
                    send_props.card_page.cdb = response.data[0][0];
                } catch (error) {}
            } as (v : string | number, id : string) => Promise<void>,
        },
        show_list : {
            cdb: true,
            card: false
        },
        uploading : false,
        get : async function () {
            try {
                let response = await axios.get('http://127.0.0.1:8000/api/get_cdbs');
                main_page.cdb.content = response.data;
                main_page.page.count[0] = main_page.cdb.content.length > 0 ? 1 : 0;
            } catch (error) {}
        } as () => Promise<void>,
        remove : async function (i) {
            main_page.cdb.content.splice(main_page.cdb.content.indexOf(send_props.list_page.cdb[0][0]), 1);
            if (Math.ceil(main_page.cdb.content.length / 10) < main_page.page.count[0])
                main_page.page.count[0] = Math.ceil(main_page.cdb.content.length / 10);
            try {
                await axios.post('http://127.0.0.1:8000/api/remove_file', {file: send_props.list_page.cdb[0][0]});
            } catch (error) {}
            whether_show_list_page();
            send_props.card_page.close = i;
        } as (i: string) => Promise<void>
    });

    let upload_file_input = ref(null);
    let upload_file = {
        click : function (e) {
            try {
                let files = e.target.files;
                if (files.length) {
                    for (let i = 0; i < files.length; i++) {
                        let file = files[i];
                        let formData = new FormData();
                        formData.append('file', file);
                        upload_file.send(formData);
                    }
                }
            } catch (error) {}
        } as (e: any) => void,
        drag : function (e) {
            let files = e.dataTransfer.files;
            if (files.length) {
                for (let i = 0; i < files.length; i++) {
                    let file = files[i];
                    if (!upload_file.check(file.type, file.name)) {
                        continue;
                    }
                    let formData = new FormData();
                    formData.append('file', file);
                    upload_file.send(formData);
                }
            }
            main_page.uploading = false;
        } as (e: any) => void,
        check : function (type, name) {
            if (type.includes('image') || type.includes('text'))
                return true;
            else if (name.endsWith('.cdb') || name.endsWith('.ypk') || name.endsWith('.zip') || name.endsWith('.tar') || name.endsWith('.tgz') || name.endsWith('.tar.gz') || name.endsWith('.7z') || name.endsWith('.rar') || name.endsWith('.lua'))
                return true;
            
            return false;
        } as (type: string, name: string) => boolean,
        send : async function (formData) {
            try {
                let response = await axios.post('http://127.0.0.1:8000/api/get_file', formData);
                if (response.data.endsWith('.cdb')) {
                    main_page.cdb.content.push(response.data);
                }
                if (response.data.endsWith('.jpg')) {
                    send_props.card_page.pic = response.data;
                }
                if (Math.ceil(main_page.cdb.content.length / 10) > main_page.page.count[0]) {
                    main_page.page.count[0] = Math.ceil(main_page.cdb.content.length / 10);
                }
            } catch (error) {}
        } as (formData: FormData) => Promise<void>
    }

    onMounted(() => {
        main_page.get();
    });

    function filter_input(event) {
        let input_value = event.target.value;
        let new_value = input_value.replace(/[^0-9]/, '');
        while (parseInt(new_value) > Math.ceil(main_page.cdb.content.length / 10))
            new_value = new_value.slice(0, -1);
        if (new_value == '')
            new_value = 0;
        if (parseInt(new_value) < 1 && Math.ceil(main_page.cdb.content.length / 10) > 0)
            new_value = 1;
        main_page.page.count[0] = new_value;
    }

    async function whether_show_list_page(v = -1, i : Map<string, any> = new Map().set('cdb', '').set('page', -1).set('card', -1).set('id', -1)) { 
        if (main_page.show_list.card) {
            main_page.show_list.card = false;
            send_props.card_page.cdb = '';
            send_props.list_page.select = i;
            emitter.emit('event_select_or_leave_cdb');
            await(new Promise(resolve => setTimeout(resolve, 500)));
            main_page.show_list.cdb = true;
            await(new Promise(resolve => setTimeout(resolve, 5)));
        } else {
            if (v >= 0)
                main_page.cdb.get(v);
            main_page.show_list.cdb = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            main_page.show_list.card = true;
            emitter.emit('event_select_or_leave_cdb', send_props.list_page.cdb[0][0]);
        }
    }
</script>

<style scoped>
    .main_page {
        display: flex;
        justify-content: space-between;
    }

    #main_page_left {
        width: 30vw;
        height: 100vh;
    }

    #under_list_page {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    #cdb_list {
        width: 30vw;
        height: 80vh;
    }

    #cdb_list button {
        display: grid;
        align-items:  center;

        width: 30vw;
        height: 8vh;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    #cdb_list button:hover {
        width: 31vw;
        color: white;
        background-color: green;
    }

    #upload_area {
        width: 25vw;
        height: 10vh;
        border: 2px dashed #bbbbbb;

        color: #bbbbbb;

        text-align: center;
        justify-self: center;

        cursor: pointer;
    }

    #upload_area:hover {
        border: 2px dashed black;
        color: black;
    }

    .cdb_list_btn {
        display: flex;
        align-items:  center;
    }

    .cdb_list_btn button {
        width: 10vw;
        height: 8vh;
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .cdb_list_btn span {
        width: 10vw;
        height: 8vh;
        text-align: center;
    }

    .cdb_list_btn input {
        width: 3vw;
    }

    .slide_list_page-enter-active,
    .slide_list_page-leave-active {
        transition: transform 0.5s ease;
    }

    .slide_list_page-enter-from,
    .slide_list_page-leave-to {
        transform: translateX(-100%);
    }

    .slide_list_page-enter-to,
    .slide_list_page-leave-from {
        transform: translateX(0%);
    }

    .under_list_page-enter-active,
    .under_list_page-leave-active {
        transition: transform 0.5s ease;
    }

    .under_list_page-enter-from,
    .under_list_page-leave-to {
        transform: translateX(-100%);
    }

    .under_list_page-enter-to,
    .under_list_page-leave-from {
        transform: translateX(0%);
    }
</style>