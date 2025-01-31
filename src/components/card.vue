<template>
    <div class = "card_page">
        <div id = "card_name">
            <span>卡名:&nbsp;&nbsp;</span>
            <input v-model = "card.name"/>
            <span>&nbsp;&nbsp;</span>
        <button id = "search_btn" :style="{ 'background-color': open.cdb != '' ? 'cornflowerblue' : 'gray' }" @click = "card.search()">搜索</button>
    </div>
        <div id = "card_pic">
            <img :src = "card.pic"/>
            <div id = "card_link">
                <img v-for = "(i, v) in [0, 1, 2, 3, 5, 6, 7, 8]" :src = "lists.link_pics[i]" :style = "{ 'grid-row-start': [1, 3, 5][Math.floor(i / 3)], 'grid-row-end': [1, 3, 5][Math.floor(i / 3)] + 1, 'grid-column-start': (i % 3) + 1, 'grid-column-end': (i % 3) + 2 }" v-if = "vif.show.link.chk && vif.is_type.link" @mouseover = "card.get_link.src.get(i)" @mouseleave = "card.get_link.src.reset(i)" @click = "card.get_link.link(i)"/>
            </div>
            <div>
                <button ref = "show_links_btn"
                @click = "() => { vif.show.link.chk = !vif.show.link.chk; }"
                :title = "vif.show.link.chk ? '点击隐藏连接箭头' : '点击显示连接箭头'"
                v-html = "vif.show.link.chk ? '&#10003' : '&times'"
                :style = "{ 'background-color': vif.show.link.chk ? 'green' : 'red' }"
                v-if = "vif.is_type.link"></button>
            </div>
        </div>
        <div id = "card_ot">
            <span>许可:&nbsp;&nbsp;</span>
            <select v-model = "card.ot">
                <option v-for = "(i,v) in lists.ot" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_attribute">
            <span>属性:&nbsp;&nbsp;</span>
            <select v-model = "card.attribute">
                <option v-for = "(i,v) in lists.attribute" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_level">
            <span>星级:&nbsp;&nbsp;</span>
            <select v-model = "card.level">
                <option v-for = "(i,v) in lists.level" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_race">
            <span>种族:&nbsp;&nbsp;</span>
            <select  v-model = "card.race">
                <option v-for = "(i,v) in lists.race" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_setcard">
            <span v-for = "(i, v) in Array(4).fill(0)" :key = "v" :style = "{ 'grid-row-start': v + 1, 'grid-row-end': v + 2 }">字段:&nbsp;&nbsp;</span>
            <input v-for = "(i, v) in Array(4).fill(0)" :key = "v" v-model = "card.setcard[v]" @input = "filter_input($event, ['card_setcard', v], /[^a-fA-F0-9]/g)"/>
        </div>
        <div id = "card_id">
            <span>同名卡:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_alias'])" v-model = "card.alias"/>
            <span>卡号:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_id'])" v-model = "card.id"/>
            <strong v-if = "vif.warn.same_id">*卡号已存在</strong>
        </div>
        <div id = "card_atk">
            <span>攻击力:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_atk'])" v-model = "card.atk"/>
            <span v-if = "!vif.is_type.link">守备力:&nbsp;&nbsp;</span>
            <input v-if = "!vif.is_type.link" @input = "filter_input($event, ['card_def'])" v-model = "card.def"/>
            <span v-if = "vif.is_type.pendulum">灵摆刻度:&nbsp;&nbsp;</span>
            <input v-if = "vif.is_type.pendulum" @input = "filter_input($event, ['card_pendulum'])" v-model = "card.pendulum"/>
        </div>
        <textarea id = "card_desc" v-model = "card.desc"></textarea>
        <div id = "card_box">
            <transition name = "card_type">
                <div v-if = "vif.show.type.chk" id = "card_type">
                    <button class = "unshow_rpage_btn" @click = "whether_show_rpage(false, 'type')" :title = "vif.show.type.title[1]">&gt;</button>
                    <h2>卡片类型</h2>
                    <div v-for = "(i, v) in lists.type" :key = "v"><span>{{ i[1] }}:&nbsp;</span><input type = "checkbox" v-model = "card.type[v]"/> </div>
                </div>
            </transition>
            <transition name = "card_category">
                <div v-if = "vif.show.category.chk" id = "card_category">
                    <button class = "unshow_rpage_btn" @click = "whether_show_rpage(false, 'category')" :title = "vif.show.category.title[1]">&gt;</button>
                    <h2>效果分类</h2>
                    <div v-for = "(i, v) in lists.category" :key = "v"><span>{{ i[1] }}:&nbsp;</span><input type = "checkbox" v-model = "card.category[v]"/> </div>
                </div>
            </transition>
            <transition name = "card_hint">
                <div v-if = "vif.show.hint.chk" id = "card_hint" >
                    <button class = "unshow_rpage_btn" @click = "whether_show_rpage(false, 'hint')" :title = "vif.show.hint.title[1]">&gt;</button>
                    <h2>脚本提示文字</h2>
                    <div v-for = "(i, v) in Array(16).fill(0)" :key = "v">
                        <span>{{ v }}:&nbsp;</span><input type = "text" v-model = "card.hint[v]"/>
                    </div>
                </div>
            </transition>
            <transition name = "card_box_btn">
                <div v-if = "vif.unshow.btn" id = "card_box_btn">
                    <download/>
                    <button @click = "whether_show_rpage(true, 'type')">{{ vif.show.type.title[0] }}</button>
                    <button @click = "whether_show_rpage(true, 'category')">{{ vif.show.category.title[0] }}</button>
                    <button @click = "whether_show_rpage(true, 'hint')">{{ vif.show.hint.title[0] }}</button>
                    <button :style = "{ 'background-color': open.cdb != '' ? 'cornflowerblue' : 'gray' }" @click = "card.add()">新建</button>
                    <button :style = "{ 'background-color': card.origin_id > 0 ? 'red' : 'gray' }" @click = "card.del()">删除</button>
                    <button :style = "{ 'background-color': card.origin_id > 0 && card_count.id < 100000000 && card_count.id > 0 ? 'cornflowerblue' : 'gray' }" @click = "copy.from()">复制</button>
                    <button :style = "{ 'background-color': copy.content.length > 0 && open.cdb != '' ? 'cornflowerblue' : 'gray' }" @click = "copy.to()">黏贴</button>
                    <!-- <button style = "background-color: cornflowerblue;">设置</button> -->
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup name = "card_page" lang = "ts">
    import { ref, reactive, onMounted, watch, defineEmits, defineProps, computed, TrackOpTypes } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    import download from './download.vue'

    let lists = reactive({
        ot: [[0x0, '许可 N/A']],
        attribute: [[0x0, '属性 N/A']],
        level: [[0x0, '等级 N/A']],
        race: [[0x0, '种族 N/A']],
        type: [] as [number , string][],
        category: [] as [number , string][],
        link: [] as number[],
        link_pics: [] as string[],
        get : async function() {
            try {
                let response = await axios.get('http://127.0.0.1:8000/api/initialize')
                    lists.ot = response.data[1];
                    lists.attribute = response.data[2];
                    lists.level = response.data[3];
                    lists.link = response.data[4];
                    lists.category = response.data[5];
                    lists.race = response.data[6];
                    lists.type = response.data[7];
                    card.clear();
            } catch(error) {};
        }
    });
    
    let card = reactive({
        name : '',
        desc : '',
        pic : '/cover.png',
        id : 0,
        alias : 0,
        pendulum : 0,
        link : 0,
        origin_id : 0,
        origin_name : '',
        ot : '',
        attribute : '',
        level : '',
        race : '',
        atk : 0 as number | string,
        def : 0 as number | string,
        type : [false],
        category : [false],
        hint : [''],
        setcard : Array(4).fill('0'),
        get_link : {
            link : function(i) {
                if ((card.link & lists.link[i]) > 0)
                    card.link -= lists.link[i]
                else
                    card.link += lists.link[i]
                card.get_link.src.get(i);
            } as (i: number) => void,
            src : {
                get : function(i) {
                    if (lists.link_pics[i].endsWith('-on.png'))
                        return;
                    lists.link_pics[i] = './link-arrow/arrow-' + (i < 4? i + 1 : i) + '-on.png'
                } as (i: number) => void,
                reset : function (i) {
                    if ((card.link & lists.link[i]) == 0)
                        lists.link_pics[i] = './link-arrow/arrow-' + (i < 4? i + 1 : i) + '-off.png'
                } as (i: number) => void
            }
        },
        search : function() {
            select.id = -1;
            emit.list_page.search.to([
                card_count.id,
                card_count.ot,
                card_count.alias,
                card_count.setcard,
                card_count.type,
                card_count.atk,
                card_count.def,
                card_count.level,
                card_count.race,
                card_count.attribute,
                card_count.category,
                card_count.id,
                card.name,
                card.desc
            ].concat(card.hint));
        },
        clear : function() {
            card.name = '';
            card.ot = lists.ot[0][1] as string;
            card.attribute = lists.attribute[0][1] as string;
            card.level = lists.level[0][1] as string;
            card.race = lists.race[0][1] as string;
            card.id = 0;
            card.alias = 0;
            card.pic = '/cover.png';
            card.atk = 0;
            card.def = 0;
            card.pendulum = 0;
            card.link = 0;
            card.desc = '';
            card.type = Array(lists.type.length).fill(false);
            card.category = Array(lists.category.length).fill(false);
            card.hint = Array(16).fill('');
            card.setcard = Array(4).fill('0');
            card.origin_id = 0;
            card.origin_name = '';
            select.id = -1;
        } as () => void,
        del : async function() {
            await card.data.del();
            card.clear();
            emit.list_page.cdb_changed.to();
        } as () => void,
        add: async function() {
            let response = await card.data.add();
            await card.data.save();
            emit.list_page.cdb_changed.to(response);
        } as () => void,
        data : {
            get : async function () {
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/read_card', {
                        cdb: open.cdb,
                        id: select.id,
                    });
                    let data = response.data;
                    card.origin_id = data[0];
                    card.id = data[0];
                    card.ot = data[1];
                    card.alias = data[2];
                    card.setcard = data[3];
                    card.type = data[4];
                    card.atk = data[5];
                    card.def = data[6];
                    card.level = data[7][0];
                    card.pendulum = data[7][1];
                    card.race = data[8];
                    card.attribute = data[9];
                    card.category = data[10];
                    card.origin_name = data[12];
                    card.name = data[12];
                    card.desc = data[13];
                    card.hint = data[14];
                    card.pic = data[15];
                } catch (error) {}
            } as () => Promise<void>,
            paste : async function(i) {
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/save_cdb', {
                        data: copy.content[i][0],
                        code: copy.content[i][1],
                        cdb: open.cdb
                    });
                } catch (error) {}
            } as (i : number) => Promise<void>,
            save : async function() {
                if (select.id <= 0) return;
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/save_cdb', {
                        data: [
                            card_count.id,
                            card_count.ot,
                            card_count.alias,
                            card_count.setcard,
                            card_count.type,
                            card_count.atk,
                            card_count.def,
                            card_count.level,
                            card_count.race,
                            card_count.attribute,
                            card_count.category,
                            card_count.id,
                            card.name,
                            card.desc
                        ].concat(card.hint),
                        code: card.origin_id,
                        cdb: open.cdb
                    });
                    if (response.data == 'removed') {
                        emit.list_page.cdb_changed.to();
                    }
                } catch (error) {}
            } as () => Promise<void>,
            add : async function() {
                let id = -1;
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/add_cdb', {
                        cdb: open.cdb
                    });
                    id = response.data;
                } catch (error) {}
                return id;
            } as () => Promise<number>,
            del : async function() {
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/del_cdb', {
                        code: card.origin_id,
                        cdb: open.cdb
                    });
                } catch (error) {}
            } as () => Promise<void>
        }
    });

    let card_count = reactive({
        id : 0,
        alias : 0,
        ot : 0,
        level : 0,
        atk : 0,
        def : 0,
        setcard : 0,
        race : 0,
        attribute : 0,
        type : 0,
        category : 0,
        get : function() {
            card_count.type = 0;
            card.type.forEach((e, v) => {
                if (e) card_count.type += lists.type[v][0]
            });

            card_count.category = 0;
            card.category.forEach((e, v) => {
                if (e) card_count.category += lists.category[v][0]
            });
            card_count.id = (vif.warn.same_id || card.id.toString().length == 0 || card.id == 0 ? (card.origin_id > 10000000000 ? 0 : card.origin_id) : card.id);
            card_count.alias = (card.alias.toString().length == 0 ? 0 : card.alias);
            card_count.ot = lists.ot.find(e => e[1] == card.ot)?.[0] as number ?? 0;
            card_count.level = lists.level.find(e => e[1] == card.level)?.[0] as number ?? 0;
            card_count.race = lists.race.find(e => e[1] == card.race)?.[0] as number ?? 0;
            card_count.attribute = lists.attribute.find(e => e[1] == card.attribute)?.[0] as number ?? 0;
            card_count.atk = card.atk != '?' ? card.atk as number : -2; 
            card_count.def = (card_count.type & 0x4000000) == 0 ? (card.def != '?' ? card.def as number : -2) : card.link; 
            card_count.setcard = parseInt(card.setcard.slice().sort((a, b) => parseInt(a, 16) - parseInt(b, 16)).map(e => ('0'.repeat(4 - e.slice(0, 4).length)) + e.slice(0, 4)).join(''), 16);
        } as () => void
    });

    let vif = reactive({
        show : {
            category : {
                chk : false,
                title : ['效果分类', '隐藏效果分类']
            },
            type : {
                chk : false,
                title : ['卡片类型', '隐藏卡片类型']
            },
            hint : {
                chk : false,
                title : ['提示文字', '隐藏卡片脚本提示文字']
            },
            link : {
                chk : false,
                title : '点击隐藏连接箭头',
                content : '&#10003'
            },
        },
        unshow : {
            btn : true
        },
        is_type : {
            link : false,
            pendulum : false
        },
        warn : {
            same_id : false,
            id : ''
        }
    });

    let copy = reactive({
        content : [],
        from : async function() {
            if (card.origin_id <= 0 || card_count.id >= 100000000 || card_count.id == 0) return;
            await card.data.save();
            copy.content = [[
                [
                    card_count.id,
                    card_count.ot,
                    card_count.alias,
                    card_count.setcard,
                    card_count.type,
                    card_count.atk,
                    card_count.def,
                    card_count.level,
                    card_count.race,
                    card_count.attribute,
                    card_count.category,
                    card_count.id,
                    card.name,
                    card.desc
                ].concat(card.hint),
                card.origin_id,
                open.cdb,
            ]];
            window.alert('已复制:   ' + card.id + ' ' + card.name);
        } as () => void,
        to : async function() {
            if (copy.content.length == 0 || open.cdb == '') return;
            let same_group = [];
            for (let i = 0; i < copy.content.length; i++)
                if (open.list.flat().filter(e => e.split(' ')[0] == copy.content[i][0][0]).length > 0)
                    same_group.push(copy.content[i][0][0] + ' ' + copy.content[i][0][12]);
            if (same_group.length > 0 && !window.confirm('存在卡片冲突，是否仍要复制？\n' + same_group)) return;
            for (let i = 0; i < copy.content.length; i++)
                await card.data.paste(i);
            await card.data.save();
            emit.list_page.cdb_changed.to(copy.content[0][1]);
            copy.content = [];
        } as () => void
    });

    let show_links_btn = ref(null);

    onMounted(() => {
        for (let i = 1; i < 9; i++) {
            if (i == 5) {
                lists.link_pics.push('');
            }
            lists.link_pics.push('./link-arrow/arrow-' + i + '-off.png');
        }
        lists.get();
    });

    watch(card, (n) => {
        if (open.list.flat().filter(e => e.split(' ')[0] == n.id).length > 0 && card.origin_id != n.id) {
            vif.warn.same_id = true;
        } else if (vif.warn.same_id) {
            vif.warn.same_id = false;
        }

        card_count.get();

        vif.is_type.link = (card_count.type & 0x4000000) > 0;

        if ((card_count.type & 0x1000000) > 0) {
            card_count.level = parseInt((card_count.level).toString())
            card_count.level |= (card.pendulum << 16);
            card_count.level |= (card.pendulum << 24);
            vif.is_type.pendulum = true;
        } else { vif.is_type.pendulum = false; }

        emit.list_page.card_changed.to(vif.warn.same_id ? card.origin_id : card.id, card.name);
        
    }, { deep: true });

    let open = reactive({
        cdb : '',
        list : []
    });

    let select = reactive({
        id : -1
    });

    let emit = {
        main_page : {
            cdb_closed : {
                on : function() {
                    card.data.save();
                    card.clear();
                    open.cdb = '';
                    open.list = [];
                } as () => void
            },
            cdb_opened  : {
                on : function(cdb) {
                    open.cdb = cdb[0][0];
                    open.list = cdb;
                } as () => void
            }
        },
        list_page : {
            select_card : {
                on : async function (i : Map<string, any> = new Map().set('id', -1)) {
                    if (select.id >= 0)
                        await card.data.save();
                    select.id = i.get('id');

                    if (select.id < 0)
                        card.clear();
                    else
                        await card.data.get();

                    emit.list_page.get_over.to();
                } as (i : Map<string, any>) => Promise<void>
            },
            card_changed : {
                to : function (id, name) {
                    emitter.emit('to_lpage_card_changed', id.toString() + ' ' + name);
                } as (id: number, name: string) => void
            },
            cdb_changed : {
                to : function (id = -1) {
                    emitter.emit('to_lpage_cdb_changed', id);
                } as (id ?: number) => void,
                on : function (cdb) {
                    open.list = cdb;
                } as (cdb: any[]) => void
            },
            get_over : {
                to : function() {
                    emitter.emit('to_lpage_get_over');
                }
            },
            search : {
                to : function(str) {
                    emitter.emit('to_lpage_search', str);
                } as (str: any[]) => void
            }
        },
        download_page : {
            save : {
                on : async function() {
                    await card.data.save();
                    emit.download_page.save.to();
                } as () => Promise<void>,
                to : function() {
                    emitter.emit('to_dpage_save');
                } as () => void
            }
        }
    }

    emitter.on('to_cpage_cdb_closed', emit.main_page.cdb_closed.on);
    emitter.on('to_cpage_cdb_opened', emit.main_page.cdb_opened.on);
    emitter.on('to_cpage_cdb_changed', emit.list_page.cdb_changed.on);
    emitter.on('to_cpage_send_select', emit.list_page.select_card.on);
    emitter.on('to_cpage_save', emit.download_page.save.on);

    function filter_input(event, t, str_filter = /[^0-9]/) {
        let input_value = event.target.value;
        let new_value = input_value.replace(str_filter, '')
        switch (t[0]) {
            case'card_setcard':
                card.setcard[t[1]] = new_value.slice(0, 4);
                break;
            case 'card_id':
                card.id = new_value.slice(0, 9);
                break;
            case 'card_alias':
                card.alias = new_value.slice(0, 9);
                break;
            case 'card_atk':
                if (input_value.slice(0, 1) == '-' || input_value.slice(0, 1) == '?') {
                    card.atk = '?';
                } else {
                    card.atk = new_value.slice(0, 19);
                }
                break;
            case 'card_def':
                if (input_value.slice(0, 1) == '-' || input_value.slice(0, 1) == '?') {
                    card.def = '?';
                } else {
                    card.def = new_value.slice(0, 19);
                }
                break;
            case 'card_pendulum':
                while (new_value != '' && parseInt(new_value) > 15)
                    new_value = new_value.slice(0, -1);
                card.pendulum = new_value;
                break;
        }
    }

    async function whether_show_rpage(chk, v) {
        if (chk) {
            vif.unshow.btn = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            switch (v) {
                case 'category':
                    vif.show.category.chk = true;
                    break;
                case 'type':
                    vif.show.type.chk = true;
                    break;
                case 'hint':
                    vif.show.hint.chk = true;
                    break;
            }
        } else {
            switch (v) {
                case 'category':
                    vif.show.category.chk = false;
                    break;
                case 'type':
                    vif.show.type.chk = false;
                    break;
                case 'hint':
                    vif.show.hint.chk = false;
                    break;
            }
            await(new Promise(resolve => setTimeout(resolve, 500)));
            vif.unshow.btn = true;
        }
    }
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

    #search_btn {
        width: 4vw;
        height: 4vh;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;

        cursor: pointer;
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

    #card_id strong {
        color: red;
        grid-column-start: 1;
        grid-column-end: 4;
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
        max-width: 17.5vw;
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
        display: grid;

        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(16, 1fr);

        justify-items: left;
    }

    #card_category div, #card_type div {
        width: 9vw;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }

    #card_category div span, #card_type div span {
        grid-column-start: 1;
        grid-column-end: 3;
        justify-self: center;
    }

    #card_category div input, #card_type div input {
        grid-column-start: 3;
        grid-column-end: 4;
        justify-self: right;

        height: 50%;
        width: 50%;
    }

    .unshow_rpage_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: left;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;

        cursor: pointer;

        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 1;
        grid-row-end: 2;
    }

    #card_hint {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(17, 1fr);

        justify-items: left;
    }

    #card_category h2, #card_type h2, #card_hint h2 {
        justify-self: center;
        grid-column-start: 1;
        grid-column-end: 4;
        grid-row-start: 1;
        grid-row-end: 2;
    }

    #card_type, #card_category, #card_hint {
        width: 30vw;
        height: 100vh;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        justify-self: center;
    }

    #card_hint div {
        width: 100%;
        grid-column-start: 1;
        grid-column-end: 4;

        display: grid;
        grid-template-columns: repeat(6, 1fr);
        justify-items: center;
    }

    #card_hint div span {
        align-self: center;
        font-size: 120%;
        grid-column-start: 1;
        grid-column-end: 2;
    }

    #card_hint div input {
        grid-column-start: 2;
        grid-column-end: 7;

        width: 100%;
        height: 80%;
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
