<template>
    <div class = "main_page">
        <div id = "main_page_left">
            <transition name = "slide_list_page">
                <list_page v-if = "main_page.show_list.card" @event_close_cdb = "remove_cdb_from_list" @event_unshow_list_page = "whether_show_list_page" :cdb = "send_props.list_page.cdb" :selected = "send_props.list_page.select"/>
            </transition>
            <transition name = "under_list_page">
                <div v-if = "main_page.show_list.cdb" id = "under_list_page">
                    <div id = "upload_area" @dragenter.prevent="main_page.uploading = true" @dragover.prevent="main_page.uploading = true" @dragleave.prevent="main_page.uploading = false" @drop.prevent="upload_file" @click="() => { upload_file_input.click(); }">
                        <h4>拖拽文件或点击此处上传文件</h4>
                        <input type = "file" multiple accept="image/*, text/*, .lua, .cdb, .ypk, .zip, .tar, .tgz, .tar.gz, .7z, .rar" ref = "upload_file_input" @change = "click_upload_file" style = "display: none;"/>
                    </div>
                    <div id = "cdb_list">
                        <button v-for="(i, v) in (main_page.page[0] > 0? Array(main_page.cdb.length >= main_page.page[0] * 10? 10 : main_page.cdb.length % 10) : [])" :key="v" @click = "whether_show_list_page(v)">{{ main_page.cdb[v + (Math.abs(main_page.page[0]) - 1) * 10] }}</button>
                    </div>
                    <div class = "cdb_list_btn">
                        <button ref = "prev_btn" @click = "previous_page">上一页</button>
                        <span>第<input @input = "filter_input($event)" v-model = "main_page.page[0]"/>页<br>共{{ Math.ceil(main_page.cdb.length / 10) }}页</span>
                        <button ref = "next_btn" @click = "next_page">下一页</button>
                    </div>
                </div>
            </transition>
        </div>
        <card_page :pic = "send_props.card_page.pic" :close = "send_props.card_page.close" @event_close_fixed = "() => { send_props.card_page.close = '' }" @event_change_menu = "get_new_cdb_menu"/>
    </div>
</template>

<script setup lang = "ts">
    import list_page from './components/list.vue'
    import card_page from './components/card.vue'

    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    let send_props = reactive({
        card_page: {
            cdb: ['暂未打开cdb'],
            page: 0,
            card: 0,
            pic: '',
            close: ''
        },
        list_page: {
            cdb: ['暂未打开cdb'],
            select : new Map().set('cdb', '').set('page', -1).set('card', -1).set('entrust', false)
        }
    });

    let main_page = reactive({
        page : [0],
        cdb : [] as string[],
        show_list : {
            cdb: true,
            card: false
        },
        uploading : false,
    });

    let upload_file_input = ref(null);
    let prev_btn = ref(null);
    let next_btn = ref(null);

    onMounted(() => {
        get_cdbs_list();
        update_button_styles();
    });

    watch(main_page.page, () => {
        update_button_styles();
    });

    function filter_input(event) {
        let input_value = event.target.value;
        let new_value = input_value.replace(/[^0-9]/, '');
        while (parseInt(new_value) >= Math.ceil(main_page.cdb.length / 10))
            new_value = new_value.slice(0, -1);
        if (new_value == '')
            new_value = 0;
        if (parseInt(new_value) < 1 && Math.ceil(main_page.cdb.length / 10) > 0)
            new_value = 1;
        main_page.page[0] = new_value;
    }

    function next_page() {
        if (main_page.page[0] < Math.ceil(main_page.cdb.length / 10)) {
            main_page.page[0] ++ ;
        }
    }

    function previous_page() {
        if (main_page.page[0] > 1) {
            main_page.page[0] -- ;
        }
    }

    function upload_file(e) {
        let files = e.dataTransfer.files;
        if (files.length) {
            for (let i = 0; i < files.length; i++) {
                let file = files[i];
                if (!check_type(file.type, file.name)) {
                    continue;
                }
                let formData = new FormData();
                formData.append('file', file);
                send_file(formData);
            }
        }
        main_page.uploading = false;
    }

    function check_type(type, name) {
        if (type.includes('image') || type.includes('text'))
            return true;
        else if (name.endsWith('.cdb') || name.endsWith('.ypk') || name.endsWith('.zip') || name.endsWith('.tar') || name.endsWith('.tgz') || name.endsWith('.tar.gz') || name.endsWith('.7z') || name.endsWith('.rar') || name.endsWith('.lua'))
            return true;
        
        return false;
    }

    function update_button_styles() {
        btn_style_change(prev_btn.value, 'green', 'white');
        btn_style_change(next_btn.value, 'green', 'white');
        if (main_page.page[0] <= 1)
            btn_style_change(prev_btn.value, 'gray', 'black');
        if (main_page.page[0] >= Math.ceil(main_page.cdb.length / 10))
            btn_style_change(next_btn.value, 'gray', 'black');
    }

    function btn_style_change(btn, btn_color, text_color) {
        if (!btn) return;
        btn.style.backgroundColor = btn_color;
        btn.style.color = text_color;
    }

    async function get_new_cdb_menu(v, id) {
        await get_cdb_menu(v);
        let c = -1;
        let p = 1;
        for (let i = 0; i < send_props.list_page.cdb.length; i++) {
            if (send_props.list_page.cdb[i].includes(id)) {
                p = i;
                c = send_props.list_page.cdb[i].indexOf(id);
                break;
            }
        }
        send_props.list_page.select.set('page', p);
        send_props.list_page.select.set('card', c);
        send_props.list_page.select.set('entrust', true);
    }
    async function whether_show_list_page(v = -1, i : Map<string, any> = new Map().set('cdb', '').set('page', -1).set('card', -1).set('btns', [])) { 
        if (main_page.show_list.card) {
            main_page.show_list.card = false;
            send_props.list_page.select = i;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            main_page.show_list.cdb = true;
            await(new Promise(resolve => setTimeout(resolve, 5)));
            update_button_styles();
        } else {
            if (v >= 0) {
                get_cdb_menu(v);
            }
            main_page.show_list.cdb = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            main_page.show_list.card = true;
        }
    }

    async function click_upload_file(e) {
        try {
            let files = e.target.files;
            if (files.length) {
                for (let i = 0; i < files.length; i++) {
                    let file = files[i];
                    let formData = new FormData();
                    formData.append('file', file);
                    send_file(formData);
                }
            }
        } catch (error) {}
    }

    async function get_cdb_menu(v : string | number) {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/get_cdb_menu', {
                cdb: ( typeof v === 'number' ? main_page.cdb[v + (Math.abs(main_page.page[0]) - 1) * 10] : v)
            });
            send_props.list_page.cdb = response.data;
        } catch (error) {}
    }

    async function send_file(formData) {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/get_file', formData);
            if (response.data.endsWith('.cdb')) {
                main_page.cdb.push(response.data);
            }
            if (response.data.endsWith('.jpg')) {
                send_props.card_page.pic = response.data;
            }
            if (Math.ceil(main_page.cdb.length / 10) > main_page.page[0]) {
                main_page.page[0] = Math.ceil(main_page.cdb.length / 10);
            }
        } catch (error) {}
    }

    async function remove_cdb_from_list(i) {
        main_page.cdb.splice(main_page.cdb.indexOf(send_props.list_page.cdb[0][0]), 1);
        if (Math.ceil(main_page.cdb.length / 10) < main_page.page[0])
            main_page.page[0] = Math.ceil(main_page.cdb.length / 10);
        try {
            await axios.post('http://127.0.0.1:8000/api/remove_file', {file: send_props.list_page.cdb[0][0]});
        } catch (error) {}
        whether_show_list_page();
        send_props.card_page.close = i;
    }

    async function get_cdbs_list() {
        try {
            let response = await axios.get('http://127.0.0.1:8000/api/get_cdbs');
            main_page.cdb = response.data;
            main_page.page[0] = main_page.cdb.length > 0 ? 1 : 0;
        } catch (error) {}
    }
    
    // async function saveFile() {
    //     try {
    //         const opts = {
    //             types: [{
    //                 description: '文件',
    //                 accept: {
    //                     'text/plain': ['.txt'],
    //                     'application/pdf': ['.pdf'],
    //                     'image/jpeg': ['.jpg', '.jpeg'],
    //                     'image/png': ['.png']
    //                 }
    //             }],
    //             excludeAcceptAllOption: true
    //         };

    //         const handle = await window.showSaveFilePicker(opts); // 打开保存文件对话框
    //         const writable = await handle.createWritable(); // 创建可写入的文件对象

    //         // 在这里写入文件内容
    //         await writable.write('这是文件的内容');
    //         await writable.close();

    //         console.log('文件保存成功');
    //         windows.alert('success');
    //     } catch (error) {
    //         console.error('文件保存失败:', error);
    //     }
    // }

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