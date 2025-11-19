import org.jetbrains.kotlin.gradle.tasks.KotlinCompile


plugins {
    kotlin("jvm")
    kotlin("plugin.serialization")
    `maven-publish`
}

group = "org.jetbrains.research.ictl"
version = "0.4.16"

val testConfig = configurations.create("testArtifacts") {
    extendsFrom(configurations["testImplementation"]) // Updated from "testCompile"
}

tasks.register("testJar", Jar::class.java) {
    dependsOn("testClasses")
    archiveClassifier.set("test")
    from(sourceSets["test"].output)
}

artifacts {
    add("testArtifacts", tasks.named<Jar>("testJar").get()) // Added .get() for compatibility
}

dependencies {
    implementation("org.apache.commons:commons-text:1.9")
    implementation("org.jgrapht:jgrapht-core:1.5.1")
    implementation("commons-io:commons-io:2.6")
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}
