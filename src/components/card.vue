<template>
    <div class = "card_page">
        <div id = "card_name">
            <span>卡名:&nbsp;&nbsp;</span>
            <input v-model = "card_name"/>
        </div>
        <div id = "card_pic">
            <img :src = "card_pic"/>
            <div id = "card_link"><img v-for = "(i, v) in [0, 1, 2, 3, 5, 6, 7, 8]" :src = "link_list[i]" :style = "{ 'grid-row-start': [1, 3, 5][Math.floor(i / 3)], 'grid-row-end': [1, 3, 5][Math.floor(i / 3)] + 1, 'grid-column-start': (i % 3) + 1, 'grid-column-end': (i % 3) + 2 }" v-if = "whether_show_links[1]"/></div>
            <div>
                <button ref = "show_links_btn" @click = "whether_show_or_not_links" :title = "whether_show_links[0]" v-html = " whether_show_links[2] "></button>
            </div>
        </div>
        <div id = "card_ot">
            <span>许可:&nbsp;&nbsp;</span>
            <select v-model = "card_ot">
                <option v-for = "(i,v) in ot_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_attribute">
            <span>属性:&nbsp;&nbsp;</span>
            <select v-model = "card_attribute">
                <option v-for = "(i,v) in attribute_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_level">
            <span>星级:&nbsp;&nbsp;</span>
            <select v-model = "card_level">
                <option v-for = "(i,v) in level_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_race">
            <span>种族:&nbsp;&nbsp;</span>
            <select  v-model = "card_race">
                <option v-for = "(i,v) in race_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_setcard">
            <span v-for = "(i, v) in Array(4).fill(0)" :key = "v" :style = "{ 'grid-row-start': v + 1, 'grid-row-end': v + 2 }">字段:&nbsp;&nbsp;</span>
            <input v-for = "(i, v) in Array(4).fill(0)" :key = "v" v-model = "card_setcard[v]" @input = "filter_input($event, ['card_setcard', v], /[^a-fA-F0-9]/g)"/>
        </div>
        <div id = "card_id">
            <span>同名卡:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_id_II'])" v-model = "card_id_II"/>
            <span>卡号:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_id'])" v-model = "card_id"/>
        </div>
        <div id = "card_atk">
            <span>攻击力:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_atk'])" v-model = "card_atk"/>
            <span>守备力:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_def'])" v-model = "card_def"/>
            <span>灵摆刻度:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_pendulum'])" v-model = "card_pendulum"/>
        </div>
        <textarea id = "card_desc" v-model = "card_desc"></textarea>
        <div id = "card_box">
            <transition name = "card_type">
                <div v-if = "show_card_box[0][0]" id = "card_type">
                    <span v-for = "(i, v) in type_list" :key = "v" :style = "{ 'grid-column-start': [1, 3, 5][v % 3], 'grid-column-end': [1, 3, 5][v % 3] + 1, 'grid-row-start': Math.floor(v / 3) + 1, 'grid-row-end': Math.floor(v / 3) + 2 }">{{ i[1] }}:&nbsp;</span>
                    <input type = "checkbox" v-for = "(i, v) in type_list" :key = "v" v-model = "card_type[v]" :style = "{ 'grid-column-start': [1, 3, 5][v % 3] + 1, 'grid-column-end': [1, 3, 5][v % 3] + 2, 'grid-row-start': Math.floor(v / 3) + 1, 'grid-row-end': Math.floor(v / 3) + 2 }"/>
                </div>
            </transition>
            <transition name = "card_category">
                <div v-if = "show_card_box[0][1]" id = "card_category">
                    <span v-for = "(i, v) in category_list" :key = "v" :style = "{ 'grid-column-start': [1, 3, 5][v % 3], 'grid-column-end': [1, 3, 5][v % 3] + 1, 'grid-row-start': Math.floor(v / 3) + 1, 'grid-row-end': Math.floor(v / 3) + 2 }">{{ i[1] }}:&nbsp;</span>
                    <input type = "checkbox" v-for = "(i, v) in category_list" :key = "v" v-model = "card_category[v]" :style = "{ 'grid-column-start': [1, 3, 5][v % 3] + 1, 'grid-column-end': [1, 3, 5][v % 3] + 2, 'grid-row-start': Math.floor(v / 3) + 1, 'grid-row-end': Math.floor(v / 3) + 2 }"/>
                </div>
            </transition>
            <transition name = "card_hint">
                <div v-if = "show_card_box[0][2]" id = "card_hint">
                    <span id = "card_hint_title">脚本提示文字:&nbsp;</span>
                    <span class = 'card_hint_I' v-for = "(i, v) in Array(8).fill(0)" :key = "v" :style = "{ 'grid-row-start': v + 2, 'grid-row-end': v + 3 }">{{ v }}:&nbsp;</span>
                    <input class = 'card_hint_I' v-for = "(i, v) in Array(8).fill(0)" :key = "v"  v-model = "card_hint[v]" :style = "{ 'grid-row-start': v + 2, 'grid-row-end': v + 3 }"/>
                    <span class = 'card_hint_II' v-for = "(i, v) in Array(8).fill(0)" :key = "v" :style = "{ 'grid-row-start': v + 2, 'grid-row-end': v + 3 }">{{ v + 8 }}:&nbsp;</span>
                    <input class = 'card_hint_II' v-for = "(i, v) in Array(8).fill(0)" :key = "v"  v-model = "card_hint[v + 8]" :style = "{ 'grid-row-start': v + 2, 'grid-row-end': v + 3 }"/>
                </div>
            </transition>
            <transition name = "card_box_btn">
                <div v-if = "!show_card_box[0][0] &&!show_card_box[0][1] &&!show_card_box[0][2]" id = "card_box_btn"><button v-for = "(i, v) in Array(3).fill(0)" :key = "v" @click = "() => { show_card_box[0][v] = true; }" :title = "show_card_box[1][v]">&lt;</button></div>
            </transition>
        </div>
    </div>
</template>

<script setup name = "card_page">
    import { ref, onMounted, watch, defineEmits, defineProps } from 'vue';
    import axios from 'axios';

    let ot_list = ref([[0x0, '许可 N/A']]);
    let attribute_list = ref([[0x0, '属性 N/A']]);
    let level_list = ref([[0x0, '等级 N/A']]);
    let race_list = ref([[0x0, '种族 N/A']]);
    let type_list = ref([]);
    let category_list = ref([]);
    let link_list = ref([]);

    let card_data = ref([]);
    
    let card_name = ref('');
    let card_ot = ref(ot_list.value[0][1]);
    let card_attribute = ref(attribute_list.value[0][1]);
    let card_level = ref(level_list.value[0][1]);
    let card_race = ref(race_list.value[0][1]);
    let card_id = ref(0);
    let card_id_II = ref(0);
    let card_pic = ref('/cover.png');
    let card_atk = ref(0);
    let card_def = ref(0);
    let card_pendulum = ref(0);
    let card_desc = ref('');
    let card_type = ref([]);
    let card_category = ref([]);
    let card_hint = ref([]);
    let card_setcard = ref(Array(4).fill('0'));
    let card_link = 0;

    let whether_show_links = ref(['点击隐藏连接箭头', true, '&#10003']);
    let show_card_box = ref([[false, false, false], ['显示卡片类型', '显示卡片分类', '显示卡片脚本提示文字']]);
    let show_links_btn = ref(null);

    let get_select = defineProps(['cdb', 'page', 'card', 'close']);
    let select_card_list = ref([]);
    let close_card = ref(false);

    let emit = defineEmits(['event_close_fixed']);

    onMounted(() => {
        for (let i = 1; i < 9; i++) {
            if (i == 5) {
                link_list.value.push('');
            }
            link_list.value.push('./link-arrow/arrow' + i + '.png');
        }
        get_card_info();
    });

    watch(get_select, (new_value) => {
        close_card.value = new_value.close;
        select_card_list.value[0] = new_value.cdb;
        select_card_list.value[1] = new_value.page;
        select_card_list.value[2] = new_value.card;
    }, { immediate: true });

    watch(close_card, (n) => {
        if (n)
            clear_card();
            emit('event_close_fixed');
    }, { immediate: true });

    watch(select_card_list, (new_value) => {
        if (new_value[0] == '' || new_value[1] == 0)
            return;
        get_card_data();
    }, { immediate: true, deep: true });

    function filter_input(event, t, str_filter = /[^0-9]/) {
        if (t[0] == 'card_setcard') {
            let input_value = event.target.value;
            let new_value = input_value.replace(str_filter, '').slice(0, 4)
            card_setcard.value[t[1]] = new_value;
        } else if (t[0] == 'card_id') {
            let input_value = event.target.value;
            let new_value = input_value.replace(str_filter, '').slice(0, 19);
            card_id.value = new_value;
        } else if (t[0] == 'card_id_II') {
            let input_value = event.target.value;
            let new_value = input_value.replace(str_filter, '').slice(0, 19);
            card_id_II.value = new_value;
        } else if (t[0] == 'card_atk') {
            let input_value = event.target.value;
            let new_value = input_value.replace(str_filter, '').slice(0, 19);
            card_atk.value = new_value;
        } else if (t[0] == 'card_def') {
            let input_value = event.target.value;
            let new_value = input_value.replace(str_filter, '').slice(0, 19);
            card_def.value = new_value;
        } else if (t[0] == 'card_pendulum') {
            let input_value = event.target.value;
            let new_value = input_value.replace(str_filter, '');
            while (new_value != '' && parseInt(new_value) >= 255)
                new_value = new_value.slice(0, -1);
            card_pendulum.value = new_value;
        }
    }

    function whether_show_or_not_links() {
        whether_show_links.value[1] = !whether_show_links.value[1];
        whether_show_links.value[0] = whether_show_links.value[1] ? '点击隐藏连接箭头' : '点击显示连接箭头';
        whether_show_links.value[2] = whether_show_links.value[1] ? '&#10003' : '&times';
        if (show_links_btn.value)
            show_links_btn.value.style.backgroundColor = whether_show_links.value[1] ? 'green' : 'red';
    }

    function clear_card() {
        card_name.value = '';
        card_ot.value = ot_list.value[0][1];
        card_attribute.value = attribute_list.value[0][1];
        card_level.value = level_list.value[0][1];
        card_race.value = race_list.value[0][1];
        card_id.value = 0;
        card_id_II.value = 0;
        card_pic.value = '/cover.png';
        card_atk.value = 0;
        card_def.value = 0;
        card_pendulum.value = 0;
        card_desc.value = '';
        card_type.value = Array(type_list.value.length).fill(false);
        card_category.value = Array(category_list.value.length).fill(false);
        card_hint.value = Array(16).fill('');
        card_setcard.value = Array(4).fill(0);
        card_link = 0;
    }

    async function get_card_info() {
        await axios.get('http://127.0.0.1:8000/api/initialize')
            .then(get => {
                ot_list.value = get.data[1];
                attribute_list.value = get.data[2];
                level_list.value = get.data[3];
                category_list.value = get.data[4];
                race_list.value = get.data[5];
                type_list.value = get.data[6];
                clear_card()
            })
            .catch(error => {
            console.error('获取数据失败:', error);
        });
    }

    async function get_card_data() {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/read_card', {
                cdb: select_card_list.value[0],
                page: select_card_list.value[1],
                card: select_card_list.value[2]
            });
            let data = response.data;
            card_id.value = data[0];
            card_ot.value = data[1];
            card_id_II.value = data[2];
            card_setcard.value = data[3];
            card_type.value = data[4];
            card_atk.value = data[5];
            card_def.value = data[6];
            card_level.value = data[7][0];
            card_pendulum.value = data[7][1];
            card_race.value = data[8];
            card_attribute.value = data[9];
            card_category.value = data[10];
            card_name.value = data[12];
            card_desc.value = data[13];
            card_hint.value = data[14];
        } catch (error) {
            console.error('发送请求失败:', error);
        }
    };
</script>

<style scoped>
    .card_page {
        width: 70vw;
        height: 100vh;

        display: grid;

        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(21, 1fr);

        justify-items: left;

        row-gap: 2vh;
    }

    #card_name {
        grid-column-start: 1;
        grid-column-end: 3;

        justify-self: center;
    }

    #card_ot, #card_attribute, #card_level, #card_race, #card_setcard, #card_id, #card_atk {
        grid-column-start: 2;
        grid-column-end: 3;
    }

    #card_setcard, #card_id , #card_atk{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }

    #card_setcard span, #card_id span, #card_atk span {
        grid-column-start: 1;
        grid-column-end: 2;
    }

    #card_setcard input, #card_id input, #card_atk input {
        grid-column-start: 2;
        grid-column-end: 4;
        width: 80%;
    }

    #card_desc {
        grid-column-start: 1;
        grid-column-end: 3;

        grid-row-start: 9;
        grid-row-end: 16;

        justify-self: center;

        width: 90%;
        height: 100%;

        resize: none;
    }

    #card_pic {
        position: relative;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);

        justify-self: center;
        text-align: center;

        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 2;
        grid-row-end: 8;
    }

    #card_link {
        position: absolute;
        top: 0;
        left: -10%;

        width: 120%;
        height: 100%;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(5, 1fr);
        justify-items: center;
    }

    #card_pic img {
        height: 100%;
        width: auto;
        display: block;
    }

    #card_pic button {
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;
    }

    #card_link img {
        height: 100%;
        width: 100%;
    }

    #card_box {
        width: 32vw;
        height: 100vh;
        overflow: hidden;

        grid-column-start: 3;
        grid-column-end: 5;
        grid-row-start: 1;
        grid-row-end: 22;
    }

    #card_type, #card_category {
        height: 100%;
        width: 90%;

        display: grid;

        grid-template-columns: repeat(6, 1fr);
        grid-template-rows: repeat(8, 1fr);

        justify-items: center;
    }

    #card_type, #card_category, #card_hint {
        width: 30vw;
        height: 100vh;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        justify-self: center;
        text-align: center;
    }

    #card_hint {
        display: grid;

        grid-template-columns: repeat(6, 1fr);
        grid-template-rows: repeat(17, 1fr);

        justify-items: center;
    }

    #card_hint #card_hint_title {
        grid-column-start: 1;
        grid-column-end: 7;

        grid-row-start: 1;
        grid-row-end: 2;
    }

    #card_hint #card_hint_I {
        grid-column-start: 1;
        grid-column-end: 2;
    }

    #card_hint #card_hint_II {
        grid-column-start: 4;
        grid-column-end: 5;
    }

    #card_hint #card_hint_I {
        grid-column-start: 2;
        grid-column-end: 4;
        width: 80%;
    }

    #card_hint #card_hint_II {
        grid-column-start: 5;
        grid-column-end: 7;
        width: 80%;
    }

    #card_box_btn {
        right: 0;

        display: grid;
        grid-template-rows: repeat(3, 1fr);
        row-gap: 1vh;
    }

    #card_box_btn button {        
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

    .card_box_btn-enter-active,
    .card_box_btn-leave-active,
    .card_category-enter-active,
    .card_category-leave-active,
    .card_hint-enter-active,
    .card_hint-leave-active,
    .card_type-enter-active,
    .card_type-leave-active {
        transition: transform 0.5s ease;
    }
    .card_category-enter-from,
    .card_category-leave-to,
    .card_hint-enter-from,
    .card_hint-leave-to,
    .card_type-enter-from,
    .card_type-leave-to {
        transform: translateX(100%);
    }
    .card_category-enter-to,
    .card_category-leave-from,
    .card_hint-enter-to,
    .card_hint-leave-from,
    .card_type-enter-to,
    .card_type-leave-from {
        transform: translateX(0%);
    }

    .card_box_btn-enter-to,
    .card_box_btn-leave-from {
        transform: translateX(0%);
    }

    .card_box_btn-enter-from,
    .card_box_btn-leave-to {
        transform: translateX(100%);
    }
</style>
