using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.Script.Serialization;
using WebApplication2.Models;

namespace WebApplication2.Controllers
{
    public class TestController : ApiController
    {
       
    }
    //public String GetWeatherData()

    //{
    //    string url = "https://api.ikcrm.com/api/v2/products";
    //    WebRequest request = WebRequest.Create(url);
    //    request.Method = "get";
    //    // 添加header

    //    //读取返回消息
    //    string res = string.Empty;
    //    try
    //    {
    //        HttpWebResponse response = (HttpWebResponse)request.GetResponse();
    //        StreamReader reader = new StreamReader(response.GetResponseStream(), Encoding.UTF8);
    //        res = reader.ReadToEnd();
    //        reader.Close();
    //    }
    //    catch (Exception ex)
    //    {
    //        res = ex.ToString();
    //    }
    //    return res;
    //}
}

