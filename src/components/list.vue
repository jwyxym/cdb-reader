<template>
    <div class = "list_page">
        <div class = "list_header">
            <h1>{{ list_page.title }}</h1>
            <button id = "unshow_list_page_btn" @click = "whether_show_list_page()" title = "上一级目录">&lt;</button>
            <button id = "close_cdb_btn" @click = "close_cdb()" title = "关闭cdb">&times;</button>
        </div>
        <div class = "list_content">
            <button v-for = "(i,v) in list_page.cdb_list[list_page.page[0]]" :key = "v" @click = "set_select_card(v, $event)" :ref = "set_list_btns">{{ i }}</button>
        </div>
        <div class = "list_btn">
            <button ref = "prev_btn" @click = "previous_page">上一页</button>
            <span>第<input @input = "filter_input($event)" v-model = "list_page.page[0]"/>页<br>共{{ list_page.cdb_list.length - 1 }}页</span>
            <button ref = "next_btn" @click = "next_page">下一页</button>
        </div>
    </div>
</template>

<script setup name="list_page" lang = "ts">
    import { ref, reactive, onMounted, watch, defineEmits, defineProps, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    let list_page = reactive({
        page: [0],
        selected : {
            card: {
                id: -1,
                seq: -1
            },
            page: -1,
            cdb : ''
        },
        title: '',
        cdb_list: [],
    });

    let wait = {
        save_get : true
    }
    let entrust = {
        select : false,
        cdb : false,
        card_name : false
    }

    let prev_btn = ref(null);
    let next_btn = ref(null);
    let list_btns = [];

    let emit = defineEmits(['event_close_cdb', 'event_unshow_list_page']);

    let get_props = defineProps(['cdb', 'selected']);

    emitter.on('event_get_over', () => {
        wait.save_get = true;
    });

    emitter.on('event_card_changed', (i : Map<string, any>) => {
        if (list_page.page[0] == 0) return;
        let n = i.get('id') + ' ' + i.get('name');
        entrust.card_name = true;
        list_page.cdb_list[list_page.page[0]][list_page.selected.card.seq] = n;
    });

    onMounted(() => {
        update_button_styles();
    });

    watch(get_props, (new_value) => {
        entrust.cdb = new_value.selected.get('entrust');

        if (new_value.selected.get('cdb') != '' && !entrust.select) {
            entrust.select = true;
            list_page.selected.card.seq = new_value.selected.get('card');
            list_page.selected.card.id = list_page.selected.card.seq >= 0 ? list_page.cdb_list[list_page.page[0]][list_page.selected.card.seq] : -1;
            list_page.selected.page = new_value.selected.get('page');
            list_page.selected.cdb = new_value.selected.get('cdb');
        }

        if (new_value.cdb[0][0] != '暂未打开cdb') {
            if (!entrust.cdb) {
                entrust.cdb = true;
                list_page.title = new_value.cdb[0][0];
                list_page.cdb_list = new_value.cdb;
                list_page.page[0] = list_page.selected.page > 0 ? list_page.selected.page : 1;
                if (!entrust.card_name)
                    emitter.emit('event_select_card', new Map().set('card', list_page.selected.card.seq).set('id', list_page.selected.card.id).set('page', list_page.page[0]).set('cdb', get_props.cdb));
            } else if (entrust.cdb && !entrust.card_name) {
                list_page.selected.page = new_value.selected.get('page');
                list_page.selected.card.seq = new_value.selected.get('card');
                list_page.selected.card.id = list_page.selected.card.seq >= 0 ? list_page.cdb_list[list_page.page[0]][list_page.selected.card.seq] : -1;
                list_page.selected.cdb = new_value.cdb[0][0];
                list_page.title = new_value.cdb[0][0];
                list_page.cdb_list = new_value.cdb;
                list_page.page[0] = list_page.selected.page;
            }
        }
        if (entrust.card_name)
            entrust.card_name = false;
        else
            update_button_styles();

    }, { deep: true, immediate: true });

    watch(list_page.page, () => {
        update_button_styles();
    });

    function filter_input(event) {
        let input_value = event.target.value;
        let new_value = input_value.replace(/[^0-9]/, '');
        while (parseInt(new_value) > (list_page.cdb_list.length - 1))
            new_value = new_value.slice(0, -1);
        if (new_value == '')
            new_value = 0;
        if (parseInt(new_value) < 1 && list_page.cdb_list.length > 1)
            new_value = 1;
        list_page.page[0] = new_value;
    }

    function set_select_card(v, event) {
        if (!wait.save_get) return;
        wait.save_get = false;
        if (list_page.selected.card.seq == v && list_page.selected.page == list_page.page[0] && list_page.selected.cdb == list_page.title) {
            list_page.selected.card.seq = -1;
            list_page.selected.card.id = -1;
            list_page.selected.page = -1;
            list_page.selected.cdb = '';
        } else {
            list_page.selected.card.seq = v;
            list_page.selected.card.id = list_page.cdb_list[list_page.page[0]][v];
            list_page.selected.page = list_page.page[0];
            list_page.selected.cdb = list_page.title;
        }
        update_button_styles();
        emitter.emit('event_select_card', new Map().set('card', list_page.selected.card.seq).set('id', list_page.selected.card.id).set('page', list_page.page[0]).set('cdb', get_props.cdb));
    }

    function close_cdb() {
        if (confirm('确认关闭cdb吗，此操作可能导致数据丢失'))
            emit('event_close_cdb', list_page.selected.cdb);
    }

    function whether_show_list_page() {
        emitter.emit('event_select_card', new Map().set('card', -1).set('id', -1).set('page', list_page.page[0]).set('cdb', get_props.cdb));
        emit('event_unshow_list_page', -1, new Map().set('cdb', list_page.selected.cdb).set('page', list_page.selected.page).set('card', list_page.selected.card.seq));
    }

    function next_page() {
        if (list_page.page[0] < list_page.cdb_list.length - 1) {
            list_page.page[0] ++ ;
        }
    }

    function previous_page() {
        if (list_page.page[0] > 1) {
            list_page.page[0] -- ;
        }
    }

    function update_button_styles() {
        btn_style_change(prev_btn.value, 'green', 'white');
        btn_style_change(next_btn.value, 'green', 'white');
        if (list_page.page[0] <= 1)
            btn_style_change(prev_btn.value, 'gray', 'black');
        if (list_page.page[0] >= list_page.cdb_list.length - 1)
            btn_style_change(next_btn.value, 'gray', 'black');
        for (let i = 0; i < list_btns.length; i++) {
            if (list_page.selected.page == list_page.page[0] && list_page.selected.cdb == list_page.title && list_page.selected.card.seq == i) {
                btn_style_change(list_btns[i], 'green', 'white');
            } else {
                btn_style_change(list_btns[i], '', '');
            }
        }
    }

    function btn_style_change(btn, btn_color, text_color) {
        if (!btn) return;
        btn.style.backgroundColor = btn_color;
        btn.style.color = text_color;
    }

    function set_list_btns(el) {
        if (!el || list_btns.includes(el)) return;
        list_btns.push(el);
    }

</script>

<style scoped>
    .list_page {
        width: 30vw;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        display: grid;
    }

    .list_header {
        height: 10vh;
        width: 30vw;
        
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }

    .list_header h1 {
        grid-column-start: 1;
        grid-column-end: 4;
        grid-row-start: 1;
        grid-row-end: 3;
    }

    #unshow_list_page_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: right;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;

        cursor: pointer;
    }

    #close_cdb_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: right;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: red;

        cursor: pointer;
    }

    .list_content {
        height: 80vh;
    }

    .list_content button {
        display: grid;

        width: 30vw;
        height: 8vh;

        align-items:  center;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_content button:hover {
        width: 31vw;
        color: white;
        background-color: green;
    }

    .list_btn {
        display: flex;
        align-items:  center;
    }

    .list_btn button {
        width: 10vw;
        height: 8vh;
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_btn span {
        width: 10vw;
        height: 8vh;
        text-align: center;
    }

    .list_btn input {
        width: 3vw;
    }
</style>