using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using WebApplication2.Models;

namespace WebApplication2.Controllers
{
    public class TestController : ApiController
    {
        Test[] products = new Test[]
        {
            new Test { id = 1,name = "ceshi1" },
            new Test { id = 2,name = "ceshi2" },
            new Test { id = 3,name = "ceshi3" },
        };

        public IEnumerable<Test> GetAllProducts()
        {
            return products;
        }

        public IHttpActionResult GetProduct222(int id)
        {
            var product = products.FirstOrDefault(m => m.id == id);
            if(product == null)
            {
                return NotFound();
            }
            return Ok(product);
        }

        [HttpPost]
        public IHttpActionResult PostTest([FromBody]Test t)
        {

            var product = products.FirstOrDefault(m => m.id == t.id);

            if (product == null)

            {

                return NotFound();

            }

            return Ok(product);

        }
    }
}
