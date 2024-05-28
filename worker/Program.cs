using System;
using System.Threading;
using StackExchange.Redis;
using Npgsql;

namespace Worker
{
    public class Program
    {
        private static ConnectionMultiplexer? _redisCon;
        // instancia de la interfaz IDatabase
        private static IDatabase? _redisDb;

        public static int Main(string[] args)
        {
            try
            {
                _redisCon = AbrirConexionRedis();
                _redisDb = _redisCon.GetDatabase();
                bool conexionPostgre = false;

                while (true)
                {
                    Thread.Sleep(10000);

                    // Si conexion con redis es null o no se pudo establecer conexion - Reintentar conexion
                    if (_redisCon == null || !_redisCon.IsConnected)
                    {
                        Console.WriteLine("Reconectando con Redis...");
                        _redisCon = AbrirConexionRedis();
                        _redisDb = _redisCon.GetDatabase();
                    }
                    Console.WriteLine(_redisDb);
                    if (!conexionPostgre)
                    {
                        ConexionPostgreSQL();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        private static bool ConexionPostgreSQL()
        {
            // establecer ruta de conexion con PostgreSQL
            var conexion = "Host=localhost;Username=postgres;Password=password;Database=recomendaciones_videos";
            Console.WriteLine($"Conexion con Postgre: {conexion}");

            using (var conn = new NpgsqlConnection(conexion))
            {
                try
                {
                    // abrir la conexion
                    conn.Open();
                    Console.WriteLine("Conexion exitosa con Postgre");
                    return true;
                }
                catch (Exception ex)
                {
                    Console.Error.WriteLine($"Error de conexion con Postgre: {ex.Message}");
                    return false;
                }
            }    
            
        }

        private static ConnectionMultiplexer AbrirConexionRedis()
        {
            var conexion = ConfigurationOptions.Parse("localhost:6379");
            conexion.ConnectTimeout = 5000;

            while (true)
            {
                try
                {
                    Console.WriteLine("Conectando con Redis...");
                    var conexionRedis = ConnectionMultiplexer.Connect(conexion);
                    Console.WriteLine("Conexion con Redis exitosa!");
                    return conexionRedis;
                } 
                catch(RedisConnectionException)
                {
                    Console.WriteLine("Error. Intentando nuevamente conectar con Redis...");
                    Thread.Sleep(1500);
                }
            }
            
        }
    }
}
