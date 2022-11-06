import requests
import bs4
import uuid
import os

import requests_toolbelt as rt
import json
import time

from functools import partial
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoderMonitor
from requests_toolbelt import MultipartEncoder
from ProxyCloud import ProxyCloud
from utils import createID


class CallingUpload:
                def __init__(self, func,filename,args):
                    self.func = func
                    self.args = args
                    self.filename = filename
                    self.time_start = time.time()
                    self.time_total = 0
                    self.speed = 0
                    self.last_read_byte = 0
                def __call__(self,monitor):
                    try:
                        self.speed += monitor.bytes_read - self.last_read_byte
                        self.last_read_byte = monitor.bytes_read
                        tcurrent = time.time() - self.time_start
                        self.time_total += tcurrent
                        self.time_start = time.time()
                        if self.time_total>=1:
                                clock_time = (monitor.len - monitor.bytes_read) / (self.speed)
                                if self.func:
                                    self.func(self.filename,monitor.bytes_read,monitor.len,self.speed,clock_time,self.args)
                                self.time_total = 0
                                self.speed = 0
                    except:pass


async def create_session(proxy:ProxyCloud=None,username='fbdaniellee',password='laponosa'):
    HOST = 'https://repotematico.uo.edu.cu/'
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'}
    proxies = None
    if proxy:
        proxies = proxy.as_dict_proxy()
    session = requests.Session()
    user = username+createID()
    mail = f'{user}@gmail.com'
    regurl = f'{HOST}user/register'
    resp = session.get(regurl,proxies=proxies,headers=HEADERS)
    soup = BeautifulSoup(resp.text,'html.parser')
    formreg = soup.find('form',{'id':'user-register-form'})
    print(resp.text)
    inputs = formreg.find_all('input')
    b = uuid.uuid4().hex
    upload_data = {
                'timezone':(None,'America/New_York'),
                'form_build_id':(None,user),
                'form_id':(None,'user_register_form'),
                'op':(None,'Crear nueva cuenta')
                }
    for input in inputs:
        for item in upload_data:
            try:
                if item == input['name']:
                    upload_data[item] = (None,input['value'])
            except:pass
    upload_data['name'] = (None,user)
    upload_data['mail'] = (None,mail)
    upload_data['pass[pass1]'] = (None,password)
    upload_data['pass[pass2]'] = (None,password)
    encoder = rt.MultipartEncoder(upload_data)
    monitor = MultipartEncoderMonitor(encoder)
    HEADERS['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    cookies = {**resp.cookies}
    cookie = 'has_js=1; '
    for cook in cookies:
        cookie += f'{cook}={cookies[cook]}'
    #HEADERS['Cookie'] = cookie
    resp = session.post(regurl,data=upload_data,proxies=proxies,headers=HEADERS)
    log = 'No se a podido crear la session'
    if resp.url!=regurl:
        soup = BeautifulSoup(resp.text,'html.parser')
        messages = soup.find('div',{'class':'messages'})
        if messages:
            try:
                log = messages.contents[2]
            except:
                log = 'Se a creado la session correctamente'
            pass
        return RepoUploader(HOST,HEADERS,proxies,session,log)
    return None

class RepoUploaderResult(object):
    def __init__(self,url,data,uploader):
        self.id = createID()
        self.url = url
        self.data = data
        self.uploader = uploader
    async def delete(self):
        self.data['_triggering_element_name'] = (None,'field_odescarga_und_0_remove_button')
        self.data['_triggering_element_value'] = (None,'Eliminar')
        multipart_fm_data = rt.MultipartEncoder(self.data)
        monitor = MultipartEncoderMonitor(multipart_fm_data)
        self.uploader.headers['Content-Type'] = multipart_fm_data.content_type
        delurl = f'{self.uploader.host}file/ajax/field_odescarga/und/0/' + self.data['form_build_id'][1]
        resp = self.uploader.session.post(delurl,data=monitor,headers=self.uploader.headers,proxies=self.uploader.proxies)
        pass

class RepoUploader(object):
    def __init__(self,host,headers,proxies,session,log):
        self.host = host
        self.headers = headers
        self.proxies = proxies
        self.session = session
        self.log = log
        self.upload_data = None
        pass
    def upload_file(self,path,progress_func=None,progress_args=None):
        if not self.upload_data:
            urlup = f'{self.host}node/add/objetos-de-aprendizaje'
            resp = self.session.get(urlup,headers=self.headers,proxies=self.proxies)
            soup = BeautifulSoup(resp.text,'html.parser')
            form = soup.find('form',{'id':'objetos-de-aprendizaje-node-form'})
            of = open(path,'rb')
            filename = str(path).split('/')[-1]
            upload_data = {}
            upload_data['title'] = (None,'')
            upload_data['changed'] = (None,'')
            upload_data['form_build_id'] = (None,'')
            upload_data['form_token'] = (None,'')
            upload_data['form_id'] = (None,'')
            upload_data['field_oautor[und][0][value]'] = (None,'')
            upload_data['field_psubido_por[und][0][value]'] = (None,'')
        
            upload_data['field_oimagen[und][0][fid]'] = (None,'')
            upload_data['field_oimagen[und][0][display]'] = (None,'')
            upload_data['body[und][0][summary]'] = (None,'')
            upload_data['body[und][0][value]'] = (None,'')
        
            upload_data['field_pcc_by[und][0][fid]'] = (None,'')
            upload_data['field_pcc_by[und][0][display]'] = (None,'')
            upload_data['field_pcc_by_sa[und][0][fid]'] = (None,'')
            upload_data['field_pcc_by_sa[und][0][display]'] = (None,'')
            upload_data['field_pcc_by_nd[und][0][fid]'] = (None,'')
            upload_data['field_pcc_by_nd[und][0][display]'] = (None,'')
            upload_data['field_pcc_by_nc[und][0][fid]'] = (None,'')
            upload_data['field_pcc_by_nc[und][0][display]'] = (None,'')
            upload_data['field_pcc_by_nc_sa[und][0][fid]'] = (None,'')
            upload_data['field_pcc_by_nc_sa[und][0][display]'] = (None,'')
            upload_data['field_pcc_by_nc_nd[und][0][fid]'] = (None,'')
            upload_data['field_pcc_by_nc_nd[und][0][display]'] = (None,'')
            upload_data['field_pgnu_gpl[und]'] = (None,'_none')
            upload_data['field_pgpl_v1[und][0][fid]'] = (None,'')
            upload_data['field_pgpl_v1[und][0][display]'] = (None,'')
            upload_data['field_pgpl_v2[und][0][fid]'] = (None,'')
            upload_data['field_pgpl_v2[und][0][display]'] = (None,'')
            upload_data['field_pgpl_v3[und][0][fid]'] = (None,'')
            upload_data['field_pgpl_v3[und][0][display]'] = (None,'')

            upload_data['field_odescarga[und][0][fid]'] = (None,'0')
            upload_data['field_odescarga[und][0][display]'] = (None,'')
            upload_data['field_pgfdl[und][0][fid]'] = (None,'')
            upload_data['field_pgfdl[und][0][display]'] = (None,'')
            upload_data['path[alias]'] = (None,'')
        
            upload_data['ajax_page_state[css][modules/system/system.base.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/system/system.menus.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/system/system.messages.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/system/system.theme.css]'] = (None,'')
            upload_data['ajax_page_state[css][misc/ui/jquery.ui.core.css]'] = (None,'')
            upload_data['ajax_page_state[css][misc/ui/jquery.ui.theme.css]'] = (None,'')
            upload_data['ajax_page_state[css][misc/ui/jquery.ui.button.css]'] = (None,'')
            upload_data['ajax_page_state[css][misc/ui/jquery.ui.resizable.css]'] = (None,'')
            upload_data['ajax_page_state[css][misc/ui/jquery.ui.dialog.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/system/system.admin.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/system/system.admin.css]'] = (None,'')
            upload_data['ajax_page_state[css][misc/vertical-tabs.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/book/book.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/comment/comment.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/field/theme/field.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/node/node.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/search/search.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/user/user.css]'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/modules/views/css/views.css]'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/modules/ckeditor/css/ckeditor.css]'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/modules/ctools/css/ctools.css'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/modules/tagadelic/tagadelic.css]'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/modules/cycle/stylesheets/drupal-cycle.css]'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/modules/ckeditor/css/ckeditor.editor.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/filter/filter.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/file/file.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/image/image.css]'] = (None,'')
            upload_data['ajax_page_state[css][modules/image/image.css]'] = (None,'')
            upload_data['ajax_page_state[css][sites/all/themes/touch/style.css]'] = (None,'')
            upload_data['ajax_page_state[js][0]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/ckeditor/includes/ckeditor.utils.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/libraries/ckeditor/ckeditor.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/jquery/1.10/jquery.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/jquery-extend-3.4.0.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/jquery.once.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/drupal.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.core.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.widget.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.button.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.mouse.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.draggable.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.position.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.resizable.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/ui/minified/jquery.ui.dialog.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/ui/external/jquery.cookie.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/replace/misc/jquery.form.min.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/vertical-tabs.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/states.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/form.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/ajax.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/jquery_update/js/jquery_update.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/admin_menu/admin_devel/admin_devel.js]'] = (None,'')
            upload_data['ajax_page_state[js][public://languages/es_hqb_krYVjzr4GA3jB0eHRzekT05UwKk2YOZI3UdJiXA.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/progress.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/autologout/autologout.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/cycle/cycle.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/autocomplete.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/textarea.js]'] = (None,'')
            upload_data['ajax_page_state[js][modules/field/modules/text/text.js]'] = (None,'')
            upload_data['ajax_page_state[js][modules/filter/filter.js]'] = (None,'')
            upload_data['ajax_page_state[js][misc/collapse.js]'] = (None,'')
            upload_data['ajax_page_state[js][modules/file/file.js]'] = (None,'')
            upload_data['ajax_page_state[js][modules/path/path.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/modules/conditional_fields/js/conditional_fields.js]'] = (None,'')
            upload_data['ajax_page_state[js][sites/all/themes/touch/js/scrolltopcontrol.js]'] = (None,'')
            upload_data['ajax_page_state[jquery_version]'] = (None,'1.7')
            upload_data['ajax_iframe_upload'] = (None,'1')

            for data in upload_data:
                try:
                    upload_data[data] = (None,form.find('input',{'name':data})['value'])
                except:pass
                if '[css]' in data or '[js]' in data:
                    upload_data[data] = (None,'1')
                if '[fid]' in data:
                    upload_data[data] = (None,'0')
                if '[display]' in data:
                    upload_data[data] = (None,'1')

            upload_data['body[und][0][format]'] = (None,'filtered_html')
            upload_data['field_plicencia[und]'] = (None,'_none')
            upload_data['field_pcreative_commons[und]'] = (None,'_none')
            upload_data['field_ofacultad[und]'] = (None,'_none')
            upload_data['field_ongenier_a_mec_nica_e_indu[und]'] = (None,'_none')
            upload_data['field_oiencias_econ_micas_y_empr[und]'] = (None,'_none')
            upload_data['field_oingenier_a_el_ctrica[und]'] = (None,'_none')
            upload_data['field_oiencias_naturales_y_exact[und]'] = (None,'_none')
            upload_data['field_ociencias_sociales[und]'] = (None,'_none')
            upload_data['field_oconstrucci_n[und]'] = (None,'_none')
            upload_data['field_ocultura_f_sica[und]'] = (None,'_none')
            upload_data['field_oderecho[und]'] = (None,'_none')
            upload_data['field_oducaci_n_ciencias_natural[und]'] = (None,'_none')
            upload_data['field_oducaci_n_ciencias_sociale[und]'] = (None,'_none')
            upload_data['field_oeducaci_n_infantil[und]'] = (None,'_none')
            upload_data['field_ongenier_a_qu_mica_y_agron[und]'] = (None,'_none')
            upload_data['field_oasignatura[und]'] = (None,'_none')
            upload_data['field_oipo_de_objeto_de_aprendiz[und]'] = (None,'_none')
            upload_data['additional_settings__active_tab'] = (None,'edit-path')
            upload_data['_triggering_element_name'] = (None,'field_odescarga_und_0_upload_button')
            upload_data['_triggering_element_value'] = (None,'Subir al servidor')
            upload_data['ajax_html_ids[]'] = (None,'wrapper,header-top,logo,site-slogan,block-search-form,search-block-form,edit-search-block-form--2,edit-actions--2,edit-submit--2,header,main-menu,content-body,main,main-content,highlighted,block-node-recent,page-title,block-system-main,objetos-de-aprendizaje-node-form,edit-title,edit-field-oautor,field-oautor-add-more-wrapper,edit-field-oautor-und-0-value,edit-field-psubido-por,field-psubido-por-add-more-wrapper,edit-field-psubido-por-und-0-value,edit-field-ofacultad,edit-field-ofacultad-und,edit-field-ongenier-a-mec-nica-e-indu,edit-field-ongenier-a-mec-nica-e-indu-und,edit-field-oiencias-econ-micas-y-empr,edit-field-oiencias-econ-micas-y-empr-und,edit-field-oingenier-a-el-ctrica,edit-field-oingenier-a-el-ctrica-und,edit-field-oiencias-naturales-y-exact,edit-field-oiencias-naturales-y-exact-und,edit-field-ociencias-sociales,edit-field-ociencias-sociales-und,edit-field-oconstrucci-n,edit-field-oconstrucci-n-und,edit-field-ocultura-f-sica,edit-field-ocultura-f-sica-und,edit-field-oderecho,edit-field-oderecho-und,edit-field-oducaci-n-ciencias-natural,edit-field-oducaci-n-ciencias-natural-und,edit-field-oducaci-n-ciencias-sociale,edit-field-oducaci-n-ciencias-sociale-und,edit-field-oeducaci-n-infantil,edit-field-oeducaci-n-infantil-und,edit-field-ongenier-a-qu-mica-y-agron,edit-field-ongenier-a-qu-mica-y-agron-und,edit-field-oasignatura,edit-field-oasignatura-und,edit-field-oasignatura-und-autocomplete,edit-field-oasignatura-und-autocomplete-aria-live,edit-field-oipo-de-objeto-de-aprendiz,edit-field-oipo-de-objeto-de-aprendiz-und,edit-field-oimagen,edit-field-oimagen-und-0-ajax-wrapper,edit-field-oimagen-und-0-upload,edit-field-oimagen-und-0-upload-button,edit-body,body-add-more-wrapper,edit-body-und-0-summary,cke_edit-body-und-0-summary,cke_edit-body-und-0-summary_arialbl,cke_1_top,cke_13,cke_1_toolbox,cke_15,cke_16,cke_16_label,cke_17,cke_18,cke_18_label,cke_19,cke_19_label,cke_20,cke_20_label,cke_21,cke_21_label,cke_22,cke_22_label,cke_23,cke_23_label,cke_24,cke_25,cke_25_label,cke_26,cke_26_label,cke_27,cke_27_label,cke_28,cke_28_label,cke_29,cke_29_label,cke_30,cke_31,cke_31_label,cke_32,cke_32_label,cke_33,cke_33_label,cke_34,cke_34_label,cke_35,cke_35_label,cke_36,cke_36_label,cke_37,cke_38,cke_38_label,cke_39,cke_39_label,cke_40,cke_14,cke_14_label,cke_14_text,cke_41,cke_42,cke_42_label,cke_43,cke_43_label,cke_44,cke_44_label,cke_45,cke_45_label,cke_46,cke_46_label,cke_47,cke_47_label,cke_48,cke_48_label,cke_49,cke_50,cke_50_label,cke_51,cke_51_label,cke_52,cke_52_label,cke_53,cke_53_label,cke_54,cke_54_label,cke_55,cke_56,cke_56_label,cke_57,cke_57_label,cke_58,cke_58_label,cke_59,cke_59_label,cke_60,cke_60_label,cke_61,cke_61_label,cke_62,cke_63,cke_63_label,cke_64,cke_64_label,cke_65,cke_65_label,cke_1_contents,cke_71,cke_1_bottom,cke_1_resizer,cke_1_path_label,cke_1_path,edit-body-und-0-value,cke_edit-body-und-0-value,cke_edit-body-und-0-value_arialbl,cke_2_top,cke_76,cke_2_toolbox,cke_78,cke_79,cke_79_label,cke_80,cke_81,cke_81_label,cke_82,cke_82_label,cke_83,cke_83_label,cke_84,cke_84_label,cke_85,cke_85_label,cke_86,cke_86_label,cke_87,cke_88,cke_88_label,cke_89,cke_89_label,cke_90,cke_90_label,cke_91,cke_91_label,cke_92,cke_92_label,cke_93,cke_94,cke_94_label,cke_95,cke_95_label,cke_96,cke_96_label,cke_97,cke_97_label,cke_98,cke_98_label,cke_99,cke_99_label,cke_100,cke_101,cke_101_label,cke_102,cke_102_label,cke_103,cke_77,cke_77_label,cke_77_text,cke_104,cke_105,cke_105_label,cke_106,cke_106_label,cke_107,cke_107_label,cke_108,cke_108_label,cke_109,cke_109_label,cke_110,cke_110_label,cke_111,cke_111_label,cke_112,cke_113,cke_113_label,cke_114,cke_114_label,cke_115,cke_115_label,cke_116,cke_116_label,cke_117,cke_117_label,cke_118,cke_119,cke_119_label,cke_120,cke_120_label,cke_121,cke_121_label,cke_122,cke_122_label,cke_123,cke_123_label,cke_124,cke_124_label,cke_125,cke_126,cke_126_label,cke_127,cke_127_label,cke_128,cke_128_label,cke_2_contents,cke_133,cke_2_bottom,cke_2_resizer,cke_2_path_label,cke_2_path,switch_edit-body-und-0-value,edit-body-und-0-format,edit-body-und-0-format-help,edit-body-und-0-format--2,edit-body-und-0-format-guidelines,edit-field-plicencia,edit-field-plicencia-und,edit-field-pcreative-commons,edit-field-pcreative-commons-und,edit-field-pcc-by,edit-field-pcc-by-und-0-ajax-wrapper,edit-field-pcc-by-und-0-upload,edit-field-pcc-by-und-0-upload-button,edit-field-pcc-by-sa,edit-field-pcc-by-sa-und-0-ajax-wrapper,edit-field-pcc-by-sa-und-0-upload,edit-field-pcc-by-sa-und-0-upload-button,edit-field-pcc-by-nd,edit-field-pcc-by-nd-und-0-ajax-wrapper,edit-field-pcc-by-nd-und-0-upload,edit-field-pcc-by-nd-und-0-upload-button,edit-field-pcc-by-nc,edit-field-pcc-by-nc-und-0-ajax-wrapper,edit-field-pcc-by-nc-und-0-upload,edit-field-pcc-by-nc-und-0-upload-button,edit-field-pcc-by-nc-sa,edit-field-pcc-by-nc-sa-und-0-ajax-wrapper,edit-field-pcc-by-nc-sa-und-0-upload,edit-field-pcc-by-nc-sa-und-0-upload-button,edit-field-pcc-by-nc-nd,edit-field-pcc-by-nc-nd-und-0-ajax-wrapper,edit-field-pcc-by-nc-nd-und-0-upload,edit-field-pcc-by-nc-nd-und-0-upload-button,edit-field-pgnu-gpl,edit-field-pgnu-gpl-und,edit-field-pgpl-v1,edit-field-pgpl-v1-und-0-ajax-wrapper,edit-field-pgpl-v1-und-0-upload,edit-field-pgpl-v1-und-0-upload-button,edit-field-pgpl-v2,edit-field-pgpl-v2-und-0-ajax-wrapper,edit-field-pgpl-v2-und-0-upload,edit-field-pgpl-v2-und-0-upload-button,edit-field-pgpl-v3,edit-field-pgpl-v3-und-0-ajax-wrapper,edit-field-pgpl-v3-und-0-upload,edit-field-pgpl-v3-und-0-upload-button,edit-field-odescarga,edit-field-odescarga-und-0-ajax-wrapper,edit-field-odescarga-und-0-upload,edit-field-odescarga-und-0-upload-button,edit-field-pgfdl,edit-field-pgfdl-und-0-ajax-wrapper,edit-field-pgfdl-und-0-upload,edit-field-pgfdl-und-0-upload-button,active-vertical-tab,edit-path,edit-path-alias,edit-actions,edit-submit,edit-preview,sidebar-first,block-system-user-menu,block-menu-menu-men-docente,block-menu-menu-menuselect,block-menu-menu-enlaces,block-tagadelic-taxonomy-tagadelic-taxonomy,block-views-slickslideshow-block,block-my-visitors-my-visitors-block,footer,block-system-powered-by,autologout-cache-check,autologout-cache-check-bit,topcontrol')
            upload_data['ajax_page_state[theme]'] = (None,'touch')
            upload_data['ajax_page_state[theme_token]'] = (None,'')
            #self.upload_data = upload_data

        upload_data['files[field_odescarga_und_0]'] = (filename,of,'application/octet-stream')

        upurl = f'{self.host}file/ajax/field_odescarga/und/0/' + upload_data['form_build_id'][1]
        multipart_fm_data = rt.MultipartEncoder(upload_data)
        progrescall = CallingUpload(progress_func,filename,progress_args)
        callback = partial(progrescall)
        monitor = MultipartEncoderMonitor(multipart_fm_data,callback=callback)
        self.headers['Content-Type'] = multipart_fm_data.content_type
        resp = self.session.post(upurl,data=monitor,headers=self.headers,proxies=self.proxies)
        of.close()

        jsonparse = json.loads(str(resp.text).replace('<textarea>','').replace('</textarea>',''))
       
        datasoup =  BeautifulSoup(jsonparse[-1]['data'],'html.parser')

        url = datasoup.find('a')['href']

        upload_data.pop('files[field_odescarga_und_0]')

        return RepoUploaderResult(url,upload_data,self)


def progress(filename,bytes_read,len,speed,clock_time,args):
    print(f'{filename} uploading {bytes_read}/{len}')

#session = create_session()
#if session:
#    result = session.upload_file('CloudAutoDLV2.rar',progress_func=progress)
#    result.delete()
#else:
#    print(log)
