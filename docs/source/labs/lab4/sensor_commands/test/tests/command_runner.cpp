#include "gtest/gtest.h"

#include <sensor_commands/command.h>
#include <sensor_commands/command_runner.h>
#include <sensor_commands/sensor/sensor.h>
#include <sensor_commands/sensor/manager.h>
#include <testutil/rand_gen.hpp>

/** Fixture class for sensor_commands/ command_runner test */
class command_runner_fixture : public testing::Test
{
 protected:
    /* Fixture class members, accesible from test functions */
    int value;
    testutil::rand_gen rng;
    struct CommandRunner runner;
    int ret;
    struct CommandRunnerConfig config;
    
    /* Fixture class constructor */
    /* NOTE: Using reproducible random value for seed, check
     * explanation in unittest_main.cpp for more details */
    command_runner_fixture()
        : value(2), rng(rand())
    {
        std::cout << "Test fixture constructor! "<< std::endl;
        std::cout << "  RNG seed " << rng.get_seed() << std::endl;
    }

    virtual void SetUp() {
        


        std::cout << "Test fixture SetUp! "<< std::endl;
        /* NOTE: Both the constructor and SetUp methods are called for each test.
         * Check Googletest FAQ for more details on when to use each one:
         * https://github.com/google/googletest/blob/main/docs/faq.md#should-i-use-the-constructordestructor-of-the-test-fixture-or-setupteardown-ctorvssetup */
    }

    virtual void TearDown() {
        std::cout << "Test fixture TearDown! "<< std::endl;
        /* NOTE: Both the destructor and TearDown methods are called for each test.
         * Check Googletest FAQ for more details on when to use each one:
         * https://github.com/google/googletest/blob/main/docs/faq.md#should-i-use-the-constructordestructor-of-the-test-fixture-or-setupteardown-ctorvssetup */
    }
};

TEST_F(command_runner_fixture, add_random)
{
    int ret = 0;
    int out = 0;
    int num_a = (int)rng.get_rnd_u64();
    int num_b = (int)rng.get_rnd_u64();
    std::cout << "  Num A: " << num_a << std::endl;
    std::cout << "  Num B: " << num_b << std::endl;

    ret = demo_api_add(num_a + value, num_b, &out);
    ASSERT_EQ(ret, DEMO_API_OK);
    ASSERT_EQ(out, num_a + value + num_b);
}

TEST_F(command_runner_fixture, mult_random)
{
    int ret = 0;
    int out = 0;
    int num_a = (int)rng.get_rnd_u64();
    int num_b = (int)rng.get_rnd_u64();
    std::cout << "  Num A: " << num_a << std::endl;
    std::cout << "  Num B: " << num_b << std::endl;

    ret = demo_api_mult(num_a, num_b + value, &out);
    ASSERT_EQ(ret, DEMO_API_OK);
    ASSERT_EQ(out, num_a * (num_b + value));
}
